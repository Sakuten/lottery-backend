from sqlalchemy import event

from api.models import db, Classroom, Lottery, User, Error
from api.app import init_and_generate


def test_db_generate_never(client):
    """
        Test if `DB_GEN_POLICY == 'never'` is working.
        See the definition of `init_and_generate`
        for expected behavior.
    """
    with client.application.app_context():
        client.application.config['DB_FORCE_INIT'] = True
        client.application.config['DB_GEN_POLICY'] = 'never'
        init_and_generate()  # tables created, but initial data not generated

        assert len(User.query.all()) == 0
        assert len(Classroom.query.all()) == 0
        assert len(Lottery.query.all()) == 0
        assert len(Error.query.all()) == 0


def test_db_generate_first_time(client):
    """
        Test if `DB_GEN_POLICY == 'first_time'` is working.
        See the definition of `init_and_generate`
        for expected behavior.
    """
    with client.application.app_context():
        client.application.config['DB_FORCE_INIT'] = True
        client.application.config['DB_GEN_POLICY'] = 'never'
        init_and_generate()  # tables created, but initial data not generated

        client.application.config['DB_FORCE_INIT'] = False
        client.application.config['DB_GEN_POLICY'] = 'first_time'

        changed = False

        @event.listens_for(db.session, 'before_commit')
        def detect_change(*args, **kw):
            nonlocal changed
            changed = True

        init_and_generate()  # initial data generated

        assert changed
        assert len(User.query.all()) != 0
        assert len(Classroom.query.all()) != 0
        assert len(Lottery.query.all()) != 0
        assert len(Error.query.all()) != 0

        changed = False

        # initial data is already generated,
        # so does nothing
        init_and_generate()
        event.remove(db.session, 'before_commit', detect_change)

        assert not changed


def test_db_generate_always(client):
    """
        Test if `DB_GEN_POLICY == 'always'` is working.
        See the definition of `init_and_generate`
        for expected behavior.
    """
    with client.application.app_context():
        client.application.config['DB_GEN_POLICY'] = 'always'

        changed = False

        @event.listens_for(db.session, 'before_commit')
        def detect_change(*args, **kw):
            nonlocal changed
            changed = True

        # initial data is already generated,
        # However re-generates the data
        init_and_generate()
        event.remove(db.session, 'before_commit', detect_change)

        assert changed
        assert len(User.query.all()) != 0
        assert len(Classroom.query.all()) != 0
        assert len(Lottery.query.all()) != 0
        assert len(Error.query.all()) != 0
