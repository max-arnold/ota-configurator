# Copyright (c) 2004 by Stingray Software
# For license information, read file LICENSE in project top directory
#
# $Id: PDUDefs.py 77 2005-01-03 17:58:53Z stingray $
#
# SMPP Protocol parser and encoder library
# PDU Definitions

from PDU import *

#--- Specific field definitions

class SMString(OctetString):
    def decode(self, stream):
       l = self.parent.kw['sm_length']
       self.value = stream.read(l)

#--- TLV

class TLV_sc_interface_version(TLVInteger):
    Tag = 0x0210

class TLV_message_payload(TLVOctetString):
    Tag = 0x0424

class TLV_dest_port(TLVInteger2):
    Tag = 0x020B

class TLV_source_port(TLVInteger2):
    Tag = 0x020A

#--- PDU definitions

class BindTransmitter(PDU):
    message_type = 'bind_transmitter'
    PDUID = 0x2
    defs = [
        ('system_id', COctetString),
        ('password', COctetString),
        ('system_type', COctetString),
        ('interface_version', Integer1),
        ('addr_ton', Integer1),
        ('addr_npi', Integer1),
        ('address_range', COctetString)
        ]

class BindTransmitterRecv(PDU):
    message_type = 'bind_transmitter_recv'
    PDUID = 0x80000002L
    defs = [
        ('system_id', COctetString)
        ]
    tlvs = [
        ('sc_interface_version', TLV_sc_interface_version)
        ]

class BindReceiver(PDU):
    message_type = 'bind_receiver'
    PDUID = 0x1
    defs = [
        ('system_id', COctetString),
        ('password', COctetString),
        ('system_type', COctetString),
        ('interface_version', Integer1),
        ('addr_ton', Integer1),
        ('addr_npi', Integer1),
        ('address_range', COctetString)
        ]

class BindReceiverRecv(PDU):
    message_type = 'bind_receiver_recv'
    PDUID = 0x80000001L
    defs = [
        ('system_id', COctetString)
        ]
    tlvs = [
        ('sc_interface_version', TLV_sc_interface_version)
        ]

class SubmitSM(PDU):
    message_type = 'submit_sm'
    PDUID = 4
    defs = [
        ('service_type', COctetString),
        ('source_addr_ton', Integer1),
        ('source_addr_npi', Integer1),
        ('source_addr', COctetString),
        ('dest_addr_ton', Integer1),
        ('dest_addr_npi', Integer1),
        ('destination_addr', COctetString),
        ('esm_class', Integer1),
        ('protocol_id', Integer1),
        ('priority_flag', Integer1),
        ('schedule_delivery_time', COctetString),
        ('validity_period', COctetString),
        ('registered_delivery', Integer1),
        ('replace_if_present_flag', Integer1),
        ('data_coding', Integer1),
        ('sm_default_msg_id', Integer1),
        ('sm_length', Integer1),
        ('short_message', SMString)
        ]
    tlvs = [
        ('message_payload', TLV_message_payload),
	('source_port', TLV_source_port),
        ('dest_port', TLV_dest_port),
        ]

class DataSM(PDU):
    message_type = 'data_sm'
    PDUID = 0x103
    defs = [
        ('service_type', COctetString),
        ('source_addr_ton', Integer1),
        ('source_addr_npi', Integer1),
        ('source_addr', COctetString),
        ('dest_addr_ton', Integer1),
        ('dest_addr_npi', Integer1),
        ('destination_addr', COctetString),
        ('esm_class', Integer1),
        ('registered_delivery', Integer1),
        ('data_coding', Integer1),
        ]
    tlvs = [
        ('message_payload', TLV_message_payload),
        ('source_port', TLV_source_port),
        ('dest_port', TLV_dest_port),
        ]



class SubmitMulti(PDU):
    PDUID = 0x21
    defs = [
        ('service_type', COctetString),
        ('source_addr_ton', Integer1),
        ('source_addr_npi', Integer1),
        ('source_addr', COctetString),
        ('dest_addresses', MultiRecipients),
        ('esm_class', Integer1),
        ('protocol_id', Integer1),
        ('priority_flag', Integer1),
        ('schedule_delivery_time', COctetString),
        ('validity_period', COctetString),
        ('registered_delivery', Integer1),
        ('replace_if_present_flag', Integer1),
        ('data_coding', Integer1),
        ('sm_default_msg_id', Integer1),
        ('sm_length', Integer1),
        ('short_message', SMString)
        ]
    tlvs = [
        ('message_payload', TLV_message_payload)
        ]


class SubmitSMRecv(PDU):
    message_type = 'submit_sm_recv'
    PDUID = 0x80000004L
    defs = [
        ('message_id', COctetString)
        ]

class SubmitMultiRecv(PDU):
    PDUID = 0x80000021L
    defs = [
        ('message_id', COctetString)
        ]

class DeliverSM(PDU):
    message_type = 'deliver_sm'
    PDUID = 5
    defs = [
        ('service_type', COctetString),
        ('source_addr_ton', Integer1),
        ('source_addr_npi', Integer1),
        ('source_addr', COctetString),
        ('dest_addr_ton', Integer1),
        ('dest_addr_npi', Integer1),
        ('destination_addr', COctetString),
        ('esm_class', Integer1),
        ('protocol_id', Integer1),
        ('priority_flag', Integer1),
        ('schedule_delivery_time', COctetString),
        ('validity_period', COctetString),
        ('registered_delivery', Integer1),
        ('replace_if_present_flag', Integer1),
        ('data_coding', Integer1),
        ('sm_default_msg_id', Integer1),
        ('sm_length', Integer1),
        ('short_message', SMString)
        ]
    tlvs = [
        ('message_payload', TLV_message_payload)
        ]

class DeliverSMRecv(PDU):
    message_type = 'deliver_sm_recv'
    PDUID = 0x80000005L
    defs = [
        ('message_id', COctetString)
        ]

class EnquireLink(PDU):
    message_type = 'enquire_link'
    PDUID = 0x15L
    defs = []

class EnquireLinkRecv(PDU):
    message_type = 'enquire_link_recv'
    PDUID = 0x80000015L
    defs = []

class Unbind(PDU):
    PDUID = 6
    defs = []

class UnbindRecv(PDU):
    message_type = 'unbind_recv'
    PDUID = 0x80000006L
    defs = []

PDUS = {}

def _register():
  for pdu in globals().values():
    try:
      if issubclass(pdu, PDU):
        try:
          PDUS[pdu.PDUID] = pdu
        except AttributeError:
          pass
    except TypeError:
      pass

_register()
