# -*- coding: utf-8 -*-
"""
Plex Server
Who is watching what?
"""
import os
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound, Unauthorized
from plexapi.myplex import MyPlexAccount
from pkm import log, utils, SHAREDIR
from pkm.decorators import never_raise, threaded_method
from pkm.exceptions import ValidationError
from pkm.plugin import BasePlugin, BaseConfig
from pkm.filters import register_filter
from plexapi.video import Episode

NAME = 'Plex Server'


class Plugin(BasePlugin):
    DEFAULT_INTERVAL = 60

    @threaded_method
    def enable(self):
        try:
            self.plex = fetch_plex_instance(self.pkmeter)
            super(Plugin, self).enable()
        except NotFound:
            log.warning('Plex server not available.')
            return self.disable()

    @never_raise
    def update(self):
        self.data.update(plex_dict(self.plex))
        self.data['videos'] = []
        for video in self.plex.sessions():
            vinfo = {
                'user': video.usernames[0],
                'type': video.type,
                'thumb': video.thumbUrl,
                'year': video.year,
                'duration': video.duration,
                'viewoffset': video.viewOffset,
                'percent': round((video.viewOffset / video.duration) * 100),
                'player': video.players[0].device if video.players else 'NA',
                'state': video.players[0].state if video.players else 'NA',
                'title': self._video_title(video),  # keep this last
            }
            if vinfo['state'] != 'paused':
                self.data['videos'].append(vinfo)
        super(Plugin, self).update()

    def _plex_address(self):
        return 'http://%s:%s' % (self.plex.address, self.plex.port)

    def _video_title(self, video):
        if video.type == Episode.TYPE:
            return '%s s%se%s' % (video.grandparentTitle, video.seasonNumber, video.index)
        return video.title


class Config(BaseConfig):
    TEMPLATE = os.path.join(SHAREDIR, 'templates', 'plexserver_config.html')
    FIELDS = utils.Bunch(BaseConfig.FIELDS, host={}, username={'save_to_keyring':True},
        password={'save_to_keyring':True})

    def validate_password(self, field, value):
        if not value:
            return value
        try:
            MyPlexAccount.signin(self.fields.username.value, value)
            return value
        except Unauthorized:
            raise ValidationError('Invalid username or password.')

    def validate_host(self, field, value):
        if not value:
            return value
        try:
            username = self.fields.username.value
            password = self.fields.password.value
            fetch_plex_instance(self.pkmeter, username, password, value)
            return value
        except Unauthorized:
            raise ValidationError('Invalid username or password.')
        except NotFound:
            raise ValidationError('Server host or name not found.')
        except:
            raise ValidationError('Invalid server.')


def fetch_plex_instance(pkmeter, username=None, password=None, host=None):
    username = username or pkmeter.config.get('plexserver', 'username', from_keyring=True)
    password = password or pkmeter.config.get('plexserver', 'password', from_keyring=True)
    host = host or pkmeter.config.get('plexserver', 'host', '')
    if username:
        log.info('Logging into MyPlex with user %s', username)
        user = MyPlexAccount.signin(username, password)
        return user.resource(host).connect()
    log.info('Connecting to Plex host: %s', host)
    return PlexServer(host)


def plex_dict(plex):
    data = {}
    data['baseurl'] = plex._baseurl
    data['friendlyName'] = plex.friendlyName
    data['machineIdentifier'] = plex.machineIdentifier
    data['myPlex'] = plex.myPlex
    data['myPlexMappingState'] = plex.myPlexMappingState
    data['myPlexSigninState'] = plex.myPlexSigninState
    data['myPlexSubscription'] = plex.myPlexSubscription
    data['myPlexUsername'] = plex.myPlexUsername
    data['platform'] = plex.platform
    data['platformVersion'] = plex.platformVersion
    data['updatedAt'] = plex.updatedAt
    data['version'] = plex.version
    return data


@register_filter()
def plexserver_length(value):
    hours = int(value / 3600000)
    minutes = int((value - (hours * 3600000)) / 60000)
    return '%s:%02d' % (hours, minutes)
