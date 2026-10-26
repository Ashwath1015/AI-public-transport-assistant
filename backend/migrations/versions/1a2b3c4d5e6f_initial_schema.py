"""initial schema

Revision ID: 1a2b3c4d5e6f
Revises:
Create Date: 2026-10-26 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create stops table
    op.create_table(
        'stops',
        sa.Column('stop_id', sa.String, primary_key=True),
        sa.Column('stop_name', sa.String, nullable=False),
        sa.Column('stop_lat', sa.Float, nullable=False),
        sa.Column('stop_lon', sa.Float, nullable=False),
        sa.Column('location', Geometry('POINT', srid=4326)),
    )

    # Create routes table
    op.create_table(
        'routes',
        sa.Column('route_id', sa.String, primary_key=True),
        sa.Column('route_short_name', sa.String),
        sa.Column('route_long_name', sa.String),
        sa.Column('route_type', sa.Integer),
    )

    # Create trips table
    op.create_table(
        'trips',
        sa.Column('trip_id', sa.String, primary_key=True),
        sa.Column('route_id', sa.String, sa.ForeignKey('routes.route_id')),
        sa.Column('service_id', sa.String),
    )

    # Create stop_times table
    op.create_table(
        'stop_times',
        sa.Column('trip_id', sa.String, sa.ForeignKey('trips.trip_id'), primary_key=True),
        sa.Column('stop_id', sa.String, sa.ForeignKey('stops.stop_id'), primary_key=True),
        sa.Column('arrival_time', sa.String),
        sa.Column('departure_time', sa.String),
        sa.Column('stop_sequence', sa.Integer),
    )

    # Create calendar table
    op.create_table(
        'calendar',
        sa.Column('service_id', sa.String, primary_key=True),
        sa.Column('start_date', sa.Date),
        sa.Column('end_date', sa.Date),
    )

def downgrade():
    op.drop_table('calendar')
    op.drop_table('stop_times')
    op.drop_table('trips')
    op.drop_table('routes')
    op.drop_table('stops')
