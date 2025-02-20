from playhouse.postgres_ext import (
    PostgresqlExtDatabase,
    Model,
    CharField,
    TextField,
    ForeignKeyField,
    DateTimeField,
    BooleanField,
    SmallIntegerField,
    BinaryJSONField,
    TSVectorField,
    fn
)

from peewee import ModelSelect, Field, Expression
from redis import Redis

from typing import Optional, Union, List
from matplotlib.colors import cnames
from types import SimpleNamespace
from datetime import datetime
import random
import json


config = SimpleNamespace(
    redis_password='lDOUD^dQr3pVr0#ZsAmQdWi7qlA45Xw5plFFt^10J&HrLQ3#ir',
    redis_host='localhost',
    redis_port=6379,
    postgres_database_name='covid19',
    postgres_database_user='covid19',
    postgres_database_password='Vsb4k0qS9hlZP@X9$67RJ0Arx9YLL3mxngE*9d^^9Kx@6$12Tl'
)

COLORS = list(cnames.values())

def random_color():
    return random.choice(COLORS)

class PeeweeHelpers:
    @staticmethod
    def all_but(model: Model, fields: Union[Field, List[Field]]) -> List[Field]:
        if isinstance(fields, Field):
            fields = [fields]
        fields = [f.name for f in fields]

        all_but_fields = []

        for field_name in model._meta.sorted_field_names:
            if field_name not in fields:
                all_but_fields.append(
                    getattr(model, field_name)
                )

        return all_but_fields

database = PostgresqlExtDatabase(
    database=config.postgres_database_name,
    user=config.postgres_database_user,
    password=config.postgres_database_password
)
database.connect()

redis = Redis(
    host=config.redis_host,
    port=config.redis_port,
    password=config.redis_password,
    db=0
)

class BaseModel(Model):
    created = DateTimeField(default=datetime.now)

    class Meta:
        database = database

class FileType(BaseModel):
	mimetype = CharField()
	suffix = CharField()
	label = CharField()

	@classmethod
	def get_select_values(cls):
		return list(cls \
            .select(
                cls.label,
                cls.id.cast('VARCHAR').alias('value')
            ) \
            .dicts())

class Language(BaseModel):
	label = CharField()
	value = CharField()

	@classmethod
	def get_select_values(cls):
		return list(cls \
            .select(
                cls.label,
                cls.id.cast('VARCHAR').alias('value')
            ) \
            .dicts())

class Tag(BaseModel):
	text = CharField()
	color = CharField(default=random_color)

	@classmethod
	def get_select_values(cls):
		return list(cls \
            .select(
                cls.text.alias('label'),
                cls.id.cast('VARCHAR').alias('value')
            ) \
            .dicts())

class Jurisdiction(BaseModel):
	label = CharField()
	value = CharField()

	@classmethod
	def get_select_values(cls):
		return list(cls \
            .select(
                cls.label,
                cls.id.cast('VARCHAR').alias('value')
            ) \
            .dicts())

class DocumentType(BaseModel):
	label = CharField()
	value = CharField()

	@classmethod
	def get_select_values(cls):
		return list(cls \
            .select(
                cls.label,
                cls.id.cast('VARCHAR').alias('value')
            ) \
            .dicts())

class DocumentIssuer(BaseModel):
    long_name = TextField()
    short_name = CharField()

    @classmethod
    def get_values(cls) -> ModelSelect:
        num_document_versions = cls \
            .select(
                fn.COUNT(DocumentVersion.id)
            ) \
            .join(Document) \
            .join(DocumentVersion) \
            .group_by(cls.id)

        return list(cls \
            .select(
                cls,
                fn.COUNT(Document.id).alias('num_documents'),
                num_document_versions.alias('num_document_versions')
            ) \
            .join(Document) \
            .join(num_document_versions, on=(cls.id == cls.id)) \
            .group_by(cls.id) \
            .dicts())

class Document(BaseModel):
    title = TextField()
    slug = TextField()
    issuer = ForeignKeyField(DocumentIssuer, backref='documents')
    language = ForeignKeyField(Language, null=True)
    file_type = ForeignKeyField(FileType, null=True)
    source = TextField()
    source_notes = TextField(null=True)
    reviewed = BooleanField(default=False)
    flagged_for_review = BooleanField(default=False)
    has_relevant_information = BooleanField(null=True)
    is_foreign_language = BooleanField(null=True)
    is_malformed = BooleanField(null=True)
    is_empty = BooleanField(null=True)
    importance = SmallIntegerField(null=True)
    notes = TextField(null=True)
    variables = BinaryJSONField(default=lambda: {})
    search_content = TSVectorField()

    @classmethod
    def update_one(cls, data):
        document = cls.get(data.pop('document_id'))

        for field, value in data.items():
            if field in ['types', 'tags', 'jurisdictions']:
                continue
            elif field in [
                'has_relevant_information', 'is_empty',
                'is_malformed', 'is_foreign_language'
            ]:
                value = {
                    'true': True,
                    'false': False,
                    'none': None
                }.get(value)
            elif field == 'variables':
                value = json.loads(value)

            setattr(document, field, value)

        document.save()

        if 'types' in data:
            types = [(document.id, int(i)) for i in data['types']]

            DocumentDocumentTypeThroughTable \
                .delete() \
                .where(DocumentDocumentTypeThroughTable.document == document.id) \
                .execute()

            DocumentDocumentTypeThroughTable \
                .insert_many(types, fields=[
                    DocumentDocumentTypeThroughTable.document,
                    DocumentDocumentTypeThroughTable.document_type
                ]) \
                .execute()

        if 'tags' in data:
            tags = [(document.id, int(i)) for i in data['tags']]

            DocumentTagThroughTable \
                .delete() \
                .where(DocumentTagThroughTable.document == document.id) \
                .execute()

            DocumentTagThroughTable \
                .insert_many(tags, fields=[
                    DocumentTagThroughTable.document,
                    DocumentTagThroughTable.tag
                ]) \
                .execute()

        if 'jurisdictions' in data:
            jurisdictions = [(document.id, int(i)) for i in data['jurisdictions']]

            DocumentJurisdictionThroughTable \
                .delete() \
                .where(DocumentJurisdictionThroughTable.document == document.id) \
                .execute()

            DocumentJurisdictionThroughTable \
                .insert_many(jurisdictions, fields=[
                    DocumentJurisdictionThroughTable.document,
                    DocumentJurisdictionThroughTable.jurisdiction
                ]) \
                .execute()

    @classmethod
    def _selector(cls):
        document_types = Document \
            .select(
                fn.JSON_AGG(DocumentType).alias('types')
            ) \
            .join(DocumentDocumentTypeThroughTable) \
            .join(DocumentType) \
            .group_by(Document.id)

        document_jurisdictions = Document \
            .select(
                fn.JSON_AGG(Jurisdiction).alias('jurisdictions')
            ) \
            .join(DocumentJurisdictionThroughTable) \
            .join(Jurisdiction) \
            .group_by(Document.id)

        document_tags = Document \
            .select(
                fn.JSON_AGG(Tag).alias('tags')
            ) \
            .join(DocumentTagThroughTable) \
            .join(Tag) \
            .group_by(Document.id)

        return cls \
            .select(
                *PeeweeHelpers.all_but(cls, cls.search_content),
                fn.MIN(DocumentVersion.effective_date).alias('effective_date'),
                fn.MAX(DocumentVersion.termination_date).alias('termination_date'),
                fn.COUNT(DocumentVersion.id).alias('num_versions'),
                fn.ARRAY_AGG(DocumentVersion.id).alias('version_ids'),
                document_types.alias('types'),
                document_jurisdictions.alias('jurisdictions'),
                document_tags.alias('tags')
            ) \
            .join(DocumentIssuer) \
            .join_from(cls, DocumentVersion) \
            .join(document_types, on=(cls.id == cls.id)) \
            .join(document_jurisdictions, on=(cls.id == cls.id)) \
            .join(document_tags, on=(cls.id == cls.id)) \
            .group_by(cls.id, DocumentIssuer.id)

    @classmethod
    def get_one(cls, document_id: int) -> dict:
        return cls \
            ._selector() \
            .where(cls.id == document_id) \
            .first()

    @classmethod
    def get_values(
        cls,
        *,
        k: Optional[int]=None,
        n: Optional[int]=None,
        search_string: Optional[str]=None
    ) -> ModelSelect:
        selector = cls._selector()

        if search_string is not None:
            selector = selector.where(
                cls.search_content.match(search_string)
            )

        if k is not None and n is not None:
            selector = selector.paginate(k, n)

        return selector.dicts()

    @classmethod
    def get_num_pages(cls, n: int, search_string: Optional[str]=None) -> int:
        selector = cls.select(
            fn.CEIL(fn.COUNT(cls.id) / float(n))
        )

        if search_string is not None:
            selector = selector.where(
                cls.search_content.match(search_string)
            )

        return int(selector.scalar())

class DocumentVersion(BaseModel):
    title = TextField()
    slug = TextField()
    document = ForeignKeyField(Document, backref='versions')
    effective_date = DateTimeField()
    termination_date = DateTimeField(null=True)
    source = TextField()
    source_notes = TextField(null=True)
    content = TextField()
    language = ForeignKeyField(Language, null=True)
    file_type = ForeignKeyField(FileType, null=True)
    file = TextField()
    raw_file_type = CharField(null=True)
    raw_file = TextField(null=True)
    reviewed = BooleanField(default=False)
    flagged_for_review = BooleanField(default=False)
    has_relevant_information = BooleanField(null=True)
    is_foreign_language = BooleanField(null=True)
    is_malformed = BooleanField(null=True)
    is_empty = BooleanField(null=True)
    importance = SmallIntegerField(null=True)
    notes = TextField(null=True)
    variables = BinaryJSONField(default=lambda: {})
    search_content = TSVectorField()
    quick_search_content = TSVectorField(null=True)

    @classmethod
    def _selector(cls):
        document_version_tags = cls \
            .select(
                fn.JSON_AGG(Tag).alias('tags')
            ) \
            .join(DocumentVersionTagThroughTable) \
            .join(Tag) \
            .group_by(cls.id)

        document_version_types = cls \
            .select(
                fn.JSON_AGG(DocumentType).alias('types')
            ) \
            .join(DocumentVersionDocumentTypeThroughTable) \
            .join(DocumentType) \
            .group_by(cls.id)

        document_version_jurisdictions = cls \
            .select(
                fn.JSON_AGG(Jurisdiction).alias('jurisdictions')
            ) \
            .join(DocumentVersionJurisdictionThroughTable) \
            .join(Jurisdiction) \
            .group_by(cls.id)

        document_version_num = cls \
            .select(
                cls.id,
                fn \
                    .RANK() \
                    .over(
                        order_by=[cls.effective_date],
                        partition_by=[Document.id]
                    ) \
                    .alias('version_num')
            ) \
            .join(Document)

        return cls \
            .select(
                *PeeweeHelpers.all_but(cls, [
                    cls.content,
                    cls.search_content,
                    cls.quick_search_content
                ]),
                fn.ROW_TO_JSON(DocumentIssuer).alias('issuer'),
                document_version_tags.alias('tags'),
                document_version_jurisdictions.alias('jurisdictions'),
                document_version_types.alias('types'),
                fn.TO_JSON(document_version_num.c.version_num).alias('version_num')
            ) \
            .join(Document) \
            .join(DocumentIssuer) \
            .join(document_version_tags, on=(cls.id == cls.id)) \
            .join(document_version_jurisdictions, on=(cls.id == cls.id)) \
            .join(document_version_types, on=(cls.id == cls.id)) \
            .join(document_version_num, on=(DocumentVersion.id == document_version_num.c.id))

    @classmethod
    def get_one(cls, document_version_id: int) -> dict:
        return cls \
            ._selector() \
            .where(cls.id == document_version_id) \
            .first()

    @classmethod
    def get_values(
        cls,
        *,
        k: Optional[int]=None,
        n: Optional[int]=None,
        search_string: Optional[str]=None
    ) -> ModelSelect:
        selector = cls._selector()

        if search_string is not None:
            selector = selector.where(
                cls.quick_search_content.match(search_string)
            )

        if k is not None and n is not None:
            selector = selector.paginate(k, n)

        return selector.dicts()

    @classmethod
    def get_num_pages(cls, n: int, search_string: Optional[str]=None) -> int:
        selector = cls.select(
            fn.CEIL(fn.COUNT(cls.id) / float(n))
        )

        if search_string is not None:
            selector = selector.where(
                cls.quick_search_content.match(search_string)
            )

        return int(selector.scalar())

    @classmethod
    def _full_search_where(
        cls,
        search_string: str,
        *,
        regex=False,
        case_sensitive=False,
    ) -> Expression:
        if regex:
            if case_sensitive:
                where = cls.content.regexp(search_string)
            else:
                where = cls.content.iregexp(search_string)
        else:
            # escape wildcard characters
            search_string = search_string \
                .replace('%', '[%]') \
                .replace('_', '[_]') \
                .replace('[', '[[]')

            # LIKE matches the entire string
            search_string = f'%{search_string}%'

            if case_sensitive:
                where = cls.content.like(search_string)
            else:
                where = cls.content.ilike(search_string)

        return where

    @classmethod
    def full_search(
        cls,
        search_string: str,
        *,
        regex=False,
        case_sensitive=False,
        k: Optional[int]=None,
        n: Optional[int]=None
    ) -> ModelSelect:
        where = cls._full_search_where(
            search_string,
            regex=regex,
            case_sensitive=case_sensitive
        )

        selector = cls \
            .select() \
            .where(where)

        if k is not None and n is not None:
            selector = selector.paginate(k, n)

        return selector.dicts()

    @classmethod
    def full_search_num_pages(
        cls,
        search_string: str,
        n: int,
        *,
        regex=False,
        case_sensitive=False,
    ) -> int:
        where = cls._full_search_where(
            search_string,
            regex=regex,
            case_sensitive=case_sensitive
        )

        selector = cls \
            .select(
                fn.CEIL(fn.COUNT(cls.id) / float(n))
            ) \
            .where(where)

        return int(selector.scalar())

class DocumentDocumentTypeThroughTable(BaseModel):
    document_type = ForeignKeyField(DocumentType)
    document = ForeignKeyField(Document)

class DocumentTagThroughTable(BaseModel):
    document = ForeignKeyField(Document)
    tag = ForeignKeyField(Tag)

class DocumentJurisdictionThroughTable(BaseModel):
    jurisdiction = ForeignKeyField(Jurisdiction)
    document = ForeignKeyField(Document)

class DocumentVersionDocumentTypeThroughTable(BaseModel):
    document_type = ForeignKeyField(DocumentType)
    document_version = ForeignKeyField(DocumentVersion)

class DocumentVersionTagThroughTable(BaseModel):
    document_version = ForeignKeyField(DocumentVersion)
    tag = ForeignKeyField(Tag)

class DocumentVersionJurisdictionThroughTable(BaseModel):
    jurisdiction = ForeignKeyField(Jurisdiction)
    document_version = ForeignKeyField(DocumentVersion)
