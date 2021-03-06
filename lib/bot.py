#!/usr/bin/env python

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.words.protocols import irc
from bot_response import response


class Bot(irc.IRCClient):
    nickname = raw_input('Name your bot: ')
    realname = raw_input('Enter your name: ')

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)     
        print '\nConnected!'

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print 'Lost connection %s' % reason

    def signedOn(self):
        self.join(self.factory.channel)
        print 'Signed On!'

    def joined(self, channel):
        self.channel = channel
        print 'Joined %s' % channel

    def userJoined(self, user, channel):
        print 'Better look out %s just joined %s' % (user, channel)

    def userLeft(self, user, channel):
        print '%s decided they\'ve had enough of the %s madhouse' % (user, channel)

    def userQuit(self, user, quitMessage):
        print '%s has left the building -> %s' % (user, quitMessage)

    def userKicked(self, kickee, channel, kicker, message):
        print '%s showed %s the %s door %s' % (kicker, kickee, channel, message)

    def register(self, nickname, hostname='foo', servername='bar'):
        self.nickname = nickname
        if self.password is not None:
            self.sendLine("PASS %s" % self.password)
        self.setNick(nickname)
        if self.username is None:
            self.username = nickname
        self.sendLine("USER %s %s %s :%s" % 
                      (self.username, hostname, servername, self.realname))

    def irc_PING(self, prefix, params):
        print 'Ping --> %s' % params
        self.sendLine("PONG %s" % params[-1])

    def privmsg(self, user, channel, msg):
        user = user.split('!')[0]
        print '%s | %s' % (user, msg)
        if self.nickname in msg:
            answer = response()
            print '%s | %s' % (self.nickname, answer)
            self.msg(channel, answer)            
        
class Proto4Bot(ClientFactory):

    def __init__(self):
        self.channel = '#' + raw_input('Channel: ')
        self.protocol = Bot

    def clientConnectionLost(self, connector, reason):
        connector.connect()

