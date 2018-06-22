from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):

        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return



    def getGeneratorName(self):
        return "tylerptl Payload Generator"

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)


class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender      = extender
        self._helpers       = extender._helpers
        self._attack        = attack
        self.max_payloads   = 10
        self.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self, current_payload):
        # convert to string
        payload = "".join(chr(x) for x in current_payload)

        # call mutator to fuzz POST
        payload = self.mutate_payload(payload)

        #increase num of fuzzing attempts
        self.num_iterations += 1

        return payload
    def reset(self):
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):
        # pick simple mutator or call external script
        picker = random.randint(1, 3)

        offset = random.randint(0, len(original_payload)-1)
        payload = original_payload[:offset]

        # SQL injection
        if picker == 1:
            payload += "'"

        # XSS
        if picker == 2:
            payload += "<script> alert('tylerptl');</script>"

        #repeat a chunk of orig. payload random number of times
        if picker == 3:
            chunk_length = random.randint(len(payload[offset:]),len(payload)-1)
            repeat = random.randint(1, 10)

            for i in range(repeat):
                payload += original_payload[offset:offset+chunk_length]

        #add remanining bits of payload
        payload += original_payload[offset:]

        return payload

