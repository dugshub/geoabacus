"""empty message

Revision ID: f2942bfac0d7
Revises: 
Create Date: 2024-10-02 00:47:31.348214

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = 'f2942bfac0d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_geospatial_table('shapefile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('placetype', sa.String(), nullable=False),
    sa.Column('bbox', sa.String(), nullable=False),
    sa.Column('geom_type', sa.String(), nullable=False),
    sa.Column('geometry', Geometry(spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('shapefile', schema=None) as batch_op:
        batch_op.create_geospatial_index('idx_shapefile_geometry', ['geometry'], unique=False, postgresql_using='gist', postgresql_ops={})

    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['shapefile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('county',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['shapefile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hierarchy_parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hierarchy_parent_id'], ['country.id'], ),
    sa.ForeignKeyConstraint(['id'], ['shapefile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hierarchy_parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hierarchy_parent_id'], ['region.id'], ),
    sa.ForeignKeyConstraint(['id'], ['shapefile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('neighbourhood',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hierarchy_parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hierarchy_parent_id'], ['locality.id'], ),
    sa.ForeignKeyConstraint(['id'], ['shapefile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('ElementaryGeometries')
    op.drop_table('SpatialIndex')
    op.drop_table('KNN2')
    op.drop_table('data_licenses')
    op.drop_table('sql_statements_log')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sql_statements_log',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('time_start', sa.TIMESTAMP(), server_default=sa.text("'0000-01-01T00:00:00.000Z'"), nullable=False),
    sa.Column('time_end', sa.TIMESTAMP(), server_default=sa.text("'0000-01-01T00:00:00.000Z'"), nullable=False),
    sa.Column('user_agent', sa.TEXT(), nullable=False),
    sa.Column('sql_statement', sa.TEXT(), nullable=False),
    sa.Column('success', sa.INTEGER(), server_default=sa.text('0'), nullable=False),
    sa.Column('error_cause', sa.TEXT(), server_default=sa.text("'ABORTED'"), nullable=False),
    sa.CheckConstraint('success IN (0,1))', name='sqllog_success'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data_licenses',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('url', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('KNN2',
    sa.Column('db_prefix', sa.TEXT(), nullable=True),
    sa.Column('f_table_name', sa.TEXT(), nullable=True),
    sa.Column('f_geometry_column', sa.TEXT(), nullable=True),
    sa.Column('ref_geometry', sa.BLOB(), nullable=True),
    sa.Column('radius', sa.DOUBLE(), nullable=True),
    sa.Column('max_items', sa.INTEGER(), nullable=True),
    sa.Column('expand', sa.INTEGER(), nullable=True),
    sa.Column('pos', sa.INTEGER(), nullable=True),
    sa.Column('fid', sa.INTEGER(), nullable=True),
    sa.Column('distance_crs', sa.DOUBLE(), nullable=True),
    sa.Column('distance_m', sa.DOUBLE(), nullable=True)
    )
    op.create_table('SpatialIndex',
    sa.Column('f_table_name', sa.TEXT(), nullable=True),
    sa.Column('f_geometry_column', sa.TEXT(), nullable=True),
    sa.Column('search_frame', sa.BLOB(), nullable=True)
    )
    op.create_table('ElementaryGeometries',
    sa.Column('db_prefix', sa.TEXT(), nullable=True),
    sa.Column('f_table_name', sa.TEXT(), nullable=True),
    sa.Column('f_geometry_column', sa.TEXT(), nullable=True),
    sa.Column('origin_rowid', sa.INTEGER(), nullable=True),
    sa.Column('item_no', sa.INTEGER(), nullable=True),
    sa.Column('geometry', sa.BLOB(), nullable=True)
    )
    op.drop_table('neighbourhood')
    op.drop_table('locality')
    op.drop_table('region')
    op.drop_table('county')
    op.drop_table('country')
    with op.batch_alter_table('shapefile', schema=None) as batch_op:
        batch_op.drop_geospatial_index('idx_shapefile_geometry', postgresql_using='gist', column_name='geometry')

    op.drop_geospatial_table('shapefile')
    # ### end Alembic commands ###
