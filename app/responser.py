import logging
from enum import Enum

from .music import spotify, deezer, music
from emoji import emojize

logger = logging.getLogger(__name__)


class ResponseType(Enum):
    """Response types based on the available commands"""
    FROM_THE_BEGINNING = 0
    LAST_WEEK = 1


class Responser():

    def __init__(self):
        pass

    def links_by_user(self, user_links, response_type):
        msg = ''
        if response_type == ResponseType.LAST_WEEK:
            msg += '<strong>Music from the last week:</strong> \n'
        elif response_type == ResponseType.FROM_THE_BEGINNING:
            msg += '<strong>Music from the beginning of time:</strong> \n'

        for user, links in user_links.items():
            msg += '- {} <strong>{}:</strong>\n'.format(emojize(':baby:', use_aliases=True),
                                                        user.username or user.firstname)
            logger.info('User: {}, Links: {}'.format(user.id, links))
            for link in links:
                logger.info('Link: {}'.format(link.url))

                if link.link_type == spotify.LinkType.ARTIST.value:
                    msg += '    {}  {} <a href="{}">{}</a> {}\n'.format(
                        emojize(':busts_in_silhouette:', use_aliases=True),
                        '[{}{}]'.format(link.created_at.strftime(
                            "%Y/%m/%d"),
                            ' | Updated @ {} by {}'.format(link.updated_at.strftime(
                                "%Y/%m/%d"),
                                link.last_update_user.username or link.last_update_user.first_name or '') if link.last_update_user else '') if response_type == ResponseType.FROM_THE_BEGINNING else '',
                        link.url,
                        link.artist_name,
                        '({})'.format(link.genre) if link.genre is not None else '')
                elif link.link_type == spotify.LinkType.ALBUM.value:
                    msg += '    {}  {} <a href="{}">{} - {}</a> {}\n'.format(
                        emojize(':cd:', use_aliases=True),
                        '[{}{}]'.format(link.created_at.strftime(
                            "%Y/%m/%d"),
                            ' | Updated @ {} by {}'.format(link.updated_at.strftime(
                                "%Y/%m/%d"),
                                link.last_update_user.username or link.last_update_user.first_name or '') if link.last_update_user else '') if response_type == ResponseType.FROM_THE_BEGINNING else '',
                        link.url,
                        link.artist_name,
                        link.album_name,
                        '({})'.format(link.genre) if link.genre is not None else '')
                elif link.link_type == spotify.LinkType.TRACK.value:
                    msg += '    {}  {} <a href="{}">{} by {}</a> {}\n'.format(
                        emojize(':musical_note:', use_aliases=True),
                        '[{}{}]'.format(link.created_at.strftime(
                            "%Y/%m/%d"),
                            ' | Updated @ {} by {}'.format(link.updated_at.strftime(
                                "%Y/%m/%d"),
                                link.last_update_user.username or link.last_update_user.first_name or '') if link.last_update_user else '') if response_type == ResponseType.FROM_THE_BEGINNING else '',
                        link.url,
                        link.track_name,
                        link.artist_name,
                        '({})'.format(link.genre) if link.genre is not None else '')
            msg += '\n'
        return msg
