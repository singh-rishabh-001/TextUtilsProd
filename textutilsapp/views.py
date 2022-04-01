from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class ChatView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        def isDigit(x):
            try:
                x = int(x)
            except:
                return False
            return True

        chat_serializer = FileSerializer(data=request.data)
        if chat_serializer.is_valid():
            file = request.FILES['chatfile']
            chat = []
            persons = set()

            for line in file:
                line = line.decode("utf-8")
                msg = {}

                try:
                    if line == '\n':
                        # empty line ,, then append it to previous chat message
                        chat[-1]['message'] += line
                    elif (isDigit(line[0]) and line[1] == '/') or (isDigit(line[0]+line[1]) and line[2] == '/'):
                        # chat start with date and time,, it means it is a new chat
                        # splittine datetime and other
                        lineSplit = line.split(' - ')

                        datetime = lineSplit[0].split(', ')

                        # there maybe more ' - ' in the message so  join all other which are part of message
                        personMsg = " - ".join(lineSplit[1:]).split(': ')
                        msg['date'] = datetime[0]
                        msg['time'] = datetime[1]
                        if len(personMsg) < 2:
                            msg['person'] = "NULL"
                            msg['message'] = ": ".join(personMsg)
                        else:
                            msg['person'] = personMsg[0]
                            persons.add(personMsg[0])
                            msg['message'] = ": ".join(personMsg[1:])

                        if (len(chat) > 0 and chat[-1]['date'] == datetime[0]):
                            msg['showdate'] = "no"
                        else:
                            msg['showdate'] = "yes"

                        chat.append(msg)
                    else:
                        # chat not starting with date time it means it a new line message of previous message
                        chat[-1]['message'] += line
                except Exception as e:
                    print("--------------------------------------")
                    print(e)
                    print("--------------------------------------")
            return Response(data=[persons, chat], status=status.HTTP_200_OK)
        else:
            print(chat_serializer.error_messages)
            return Response(data=chat_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
