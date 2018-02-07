from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
import json
from pprint import pprint
from .models import FacebookUser
from .models import Message
from datetime import datetime
from .EmailSender import EmailSender
from .models import Ticket

# Create your views here.
from CallCenter.services import post_facebook_message

VERIFY_TOKEN = '1111'


class CallCenter(generic.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):

        self.get_message_and_show_response()

        return HttpResponse()

    def get_message_and_show_response(self):

        incoming_message = json.loads(self.request.body.decode('utf-8'))
        pprint(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    senderId = message['sender']['id']
                    currentUser = self.getOrCreateUserIfDoesNotExist(senderId)
                    lastActionForCurrentUser = self.getLastActionForCurrentUser(currentUser)
                    actionTaken = None

                    if lastActionForCurrentUser is None or lastActionForCurrentUser == 'welcome':
                        actionTaken = 'askForNumber'
                        informationMessage = 'Welcome! Please write down your number.'

                    elif lastActionForCurrentUser == 'askForNumber':
                        userNumber = currentUser.phoneNumber
                        if userNumber == message['message']['text']:
                            actionTaken = 'describeProblem'
                            informationMessage = 'Please describe your problem, so we can open a ticket for you.'
                        else:
                            actionTaken = 'numberIncorrect'
                            informationMessage = 'Incorrect number. Please try once again'

                    elif lastActionForCurrentUser == 'numberIncorrect':
                        userNumber = currentUser.phoneNumber
                        if userNumber == message['message']['text']:
                            actionTaken = 'describeProblem'
                            informationMessage = 'Please describe your problem, so we can open a ticket for you.'
                        else:
                            actionTaken = 'numberIncorrect'
                            informationMessage = 'Incorrect number. Please try once again'

                    elif lastActionForCurrentUser == 'describeProblem':
                        problemDescription = message['message']['text']
                        if problemDescription is None:
                            actionTaken = 'describeProblem'
                            informationMessage = 'You did not describe your problem. Please try once again.'
                        else:
                            actionTaken = 'welcome'
                            informationMessage = 'Your problem has been registered. Please wait for our consultant to ' \
                                                 'call you. '
                            emailSender = EmailSender()
                            emailSender.connect()
                            emailSender.send_mail('patryk.seweryn@gmail.com', message['message']['text'])
                            newTicket = Ticket(date=datetime.now(), ticketMessage=message['message']['text'], user=currentUser)
                            newTicket.save()

                    self.createMessage(currentUser, message, actionTaken)
                    post_facebook_message(senderId, informationMessage)

    def getLastActionForCurrentUser(self, currentUser):
        try:
            allMessagesOfCurrentUser = Message.objects.filter(user_id=currentUser.id).order_by('-date')
            actionOfLastMessageForCurrentUser = allMessagesOfCurrentUser[0].actionTaken
            print(actionOfLastMessageForCurrentUser)
        except Exception as e:
            actionOfLastMessageForCurrentUser = None
        return actionOfLastMessageForCurrentUser

    def createMessage(self, currentUser, message, actionTaken):
        timestamp = message['timestamp']
        dt = datetime.fromtimestamp(timestamp / 1000.0)
        currentMessage = Message(date=dt, messageText=message['message']['text'], actionTaken=actionTaken,
                                 user=currentUser)
        currentMessage.save()

    def getOrCreateUserIfDoesNotExist(self, senderId):
        try:
            user = FacebookUser.objects.get(facebookId=senderId)
        except FacebookUser.DoesNotExist:
            user = FacebookUser(facebookId=senderId)
            user.save()
        return user
