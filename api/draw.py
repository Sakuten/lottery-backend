import random
from flask import current_app
from api.models import User, Lottery, Application, db


class AlreadyDoneError(Exception):
    """
        The Exception that indicates the lottery has already done
    """
    pass


class NobodyIsApplyingError(Exception):
    """
        The Exception that indicates nobody is applying to the lottery
    """
    pass


def draw_one(lottery, raise_on_nobody=True):
    """
        Draw the specified lottery
        Args:
          lottery(Lottery): The lottery to be drawn
        Return:
          winners([User]): The list of users who won
        Raises:
            NobodyIsApplyingError, AlreadyDoneError
    """
    if lottery.done:
        raise AlreadyDoneError()

    idx = lottery.id
    applications = Application.query.filter_by(lottery_id=idx).all()
    if len(applications) == 0:
        if raise_on_nobody:
            raise NobodyIsApplyingError()
        else:
            return []
    try:
        winner_apps = random.sample(
            applications, current_app.config['WINNERS_NUM'])
    except ValueError:
        # if applications are less than WINNER_NUM, all applications are chosen
        winner_apps = applications
    for application in applications:
        application.status = "won" if application in winner_apps else "lose"
        db.session.add(application)

    lottery.done = True
    db.session.add(lottery)
    db.session.commit()
    winners = [User.query.get(winner_app.user_id)
               for winner_app in winner_apps]
    return winners


def draw_all_at_index(index):
    """
        Draw all lotteries in the specific index
        Args:
          index(int): zero-based index that indicates the time of lottery
        Return:
          winners([[User]]): The list of list of users who won
        Raises:
            NobodyIsApplyingError, AlreadyDoneError
    """
    lotteries = Lottery.query.filter_by(index=index)
    if any(lottery.done for lottery in lotteries):
        raise AlreadyDoneError()

    winners = [draw_one(lottery, raise_on_nobody=False)
               for lottery in lotteries]

    for lottery in lotteries:
        lottery.done = True
        db.session.add(lottery)
        db.session.commit()

    if len(winners) == 0:
        raise NobodyIsApplyingError()

    return winners