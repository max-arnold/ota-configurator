SMPPStatus = {
    0x00000000L : {
        'name' : 'ESME_ROK',
        'description' : 'No error',
    },
    0x00000001L : {
        'name' : 'ESME_RINVMSGLEN',
        'description': 'Message Length is invalid',
    },
    0x00000002L : {
        'name' : 'ESME_RINVCMDLEN',
        'description': 'Command Length is invalid',
    },
    0x00000003L : {
        'name' : 'ESME_RINVCMDID',
        'description': 'Invalid Command ID',
    },
    0x00000004L : {
        'name' : 'ESME_RINVBNDSTS',
        'description': 'Invalid BIND Status for given command',
    },
    0x00000005L : {
        'name' : 'ESME_RALYBND',
        'description': 'ESME Already in Bound State',
    },
    0x00000006L : {
        'name' : 'ESME_RINVPRTFLG',
        'description': 'Invalid Priority Flag',
    },
    0x00000007L : {
        'name' : 'ESME_RINVREGDLVFLG',
        'description': 'Invalid Registered Delivery Flag',
    },
    0x00000008L : {
        'name' : 'ESME_RSYSERR',
        'description': 'System Error',
    },
    0x0000000AL : {
        'name' : 'ESME_RINVSRCADR',
        'description': 'Invalid Source Address',
    },
    0x0000000BL : {
        'name' : 'ESME_RINVDSTADR',
        'description': 'Invalid Dest Addr',
    },
    0x0000000CL : {
        'name' : 'ESME_RINVMSGID',
        'description': 'Message ID is invalid',
    },
    0x0000000DL : {
        'name' : 'ESME_RBINDFAIL',
        'description': 'Bind Failed',
    },
    0x0000000EL : {
        'name' : 'ESME_RINVPASWD',
        'description': 'Invalid Password',
    },
    0x0000000FL : {
        'name' : 'ESME_RINVSYSID',
        'description': 'Invalid System ID',
    },
    0x00000011L : {
        'name' : 'ESME_RCANCELFAIL',
        'description': 'Cancel SM Failed',
    },
    0x00000013L : {
        'name' : 'ESME_RREPLACEFAIL',
        'description': 'Replace SM Failed',
    },
    0x00000014L : {
        'name' : 'ESME_RMSGQFUL',
        'description': 'Message Queue Full',
    },
    0x00000015L : {
        'name' : 'ESME_RINVSERTYP',
        'description': 'Invalid Service Type',
    },
    0x00000033L : {
        'name' : 'ESME_RINVNUMDESTS',
        'description': 'Invalid number of destinations',
    },
    0x00000034L : {
        'name' : 'ESME_RINVDLNAME',
        'description': 'Invalid Distribution List Name',
    },
    0x00000040L : {
        'name' : 'ESME_RINVDESTFLAG',
        'description': 'Destination flag is invalid (submit_multi)',
    },
    0x00000042L : {
        'name' : 'ESME_RINVSUBREP',
        'description': 'Invalid submit with replace request (i.e.  submit_sm with replace_if_present_flag set)',
    },
    0x00000043L : {
        'name' : 'ESME_RINVESMCLASS',
        'description': 'Invalid esm_class field data',
    },
    0x00000044L : {
        'name' : 'ESME_RCNTSUBDL',
        'description': 'Cannot Submit to Distribution List',
    },
    0x00000045L : {
        'name' : 'ESME_RSUBMITFAIL',
        'description': 'submit_sm or submit_multi failed',
    },
    0x00000048L : {
        'name' : 'ESME_RINVSRCTON',
        'description': 'Invalid Source address TON',
    },
    0x00000049L : {
        'name' : 'ESME_RINVSRCNPI',
        'description': 'Invalid Source address NPI',
    },
    0x00000050L : {
        'name' : 'ESME_RINVDSTTON',
        'description': 'Invalid Destination address TON',
    },
    0x00000051L : {
        'name' : 'ESME_RINVDSTNPI',
        'description': 'Invalid Destination address NPI',
    },
    0x00000053L : {
        'name' : 'ESME_RINVSYSTYP',
        'description': 'Invalid system_type field',
    },
    0x00000054L : {
        'name' : 'ESME_RINVREPFLAG',
        'description': 'Invalid replace_if_present flag',
    },
    0x00000055L : {
        'name' : 'ESME_RINVNUMMSGS',
        'description': 'Invalid number of messages',
    },
    0x00000058L : {
        'name' : 'ESME_RTHROTTLED',
        'description': 'Throttling error (ESME has exceeded allowed message limits',
    },
    0x00000061L : {
        'name' : 'ESME_RINVSCHED',
        'description': 'Invalid Scheduled Delivery Time',
    },
    0x00000062L : {
        'name' : 'ESME_RINVEXPIRY',
        'description': 'Invalid message validity period (Expiry time)',
    },
    0x00000063L : {
        'name' : 'ESME_RINVDFTMSGID',
        'description': 'Predefined Message Invalid or Not Found',
    },
    0x00000064L : {
        'name' : 'ESME_RX_T_APPN',
        'description': 'ESME Receiver Temporary App Error Code',
    },
    0x00000065L : {
        'name' : 'ESME_RX_P_APPN',
        'description': 'ESME Receiver Permanent App Error Code',
    },
    0x00000066L : {
        'name' : 'ESME_RX_P_APPN',
        'description': 'ESME Receiver Reject Message Error Code',
    },
    0x00000067L : {
        'name' : 'ESME_RQUERYFAIL',
        'description': 'query_sm request failed',
    },
    0x000000C0L : {
        'name' : 'ESME_RINVOPTPARSTREAM',
        'description': 'Error in the optional part of the PDU Body',
    },
    0x000000C1L : {
        'name' : 'ESME_ROPTPARNOTALLWD',
        'description': 'Optional Parameter not allowed',
    },
    0x000000C2L : {
        'name' : 'ESME_RINVPARLEN',
        'description': 'Invalid Parameter Length',
    },
    0x000000C3L : {
        'name' : 'ESME_RMISSINGOPTPARAM',
        'description': 'Expected Optional Parameter missing',
    },
    0x000000C4L : {
        'name' : 'ESME_RINVOPTPARAMVAL',
        'description': 'Invalid Optional Parameter Value',
    },
    0x000000FEL : {
        'name' : 'ESME_RDELIVERYFAILURE',
        'description': 'Delivery Failure (used for data_sm_resp)',
    },
    0x000000FFL : {
        'name' : 'ESME_RUNKNOWNERR',
        'description': 'Unknown Error',
    },
}
