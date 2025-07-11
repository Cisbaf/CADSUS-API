soap_body_cpf = """<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:urn="urn:ihe:iti:xds-b:2007"
                   xmlns:urn1="urn:oasis:names:tc:ebxml-regrep:xsd:lcm:3.0"
                   xmlns:urn2="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0"
                   xmlns:urn3="urn:ihe:iti:xds-b:2007"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
       <soap:Body>
          <PRPA_IN201305UV02 xsi:schemaLocation="urn:hl7-org:v3 ./schema/HL7V3/NE2008/multicacheschemas/PRPA_IN201305UV02.xsd" ITSVersion="XML_1.0" xmlns="urn:hl7-org:v3">
             <id root="2.16.840.1.113883.4.714" extension="123456"/>
             <creationTime value="20070428150301"/>
             <interactionId root="2.16.840.1.113883.1.6" extension="PRPA_IN201305UV02"/>
             <processingCode code="T"/>
             <processingModeCode code="T"/>
             <acceptAckCode code="AL"/>
             <receiver typeCode="RCV">
                <device classCode="DEV" determinerCode="INSTANCE">
                   <id root="2.16.840.1.113883.3.72.6.5.100.85"/>
                </device>
             </receiver>
             <sender typeCode="SND">
                <device classCode="DEV" determinerCode="INSTANCE">
                   <id root="2.16.840.1.113883.3.72.6.2"/>
                   <name>[SYSTEMCODE]</name>
                </device>
             </sender>
             <controlActProcess classCode="CACT" moodCode="EVN">
                <code code="PRPA_TE201305UV02" codeSystem="2.16.840.1.113883.1.6"/>
                <queryByParameter>
                   <queryId root="1.2.840.114350.1.13.28.1.18.5.999" extension="1840997084"/>
                   <statusCode code="new"/>
                   <responseModalityCode code="R"/>
                   <responsePriorityCode code="I"/>
                   <parameterList>
                      <livingSubjectId>
                         <value root="2.16.840.1.113883.13.237" extension="{{cpf_input}}"/>
                         <semanticsText>LivingSubject.id</semanticsText>
                      </livingSubjectId>
                   </parameterList>
                </queryByParameter>
             </controlActProcess>
          </PRPA_IN201305UV02>
       </soap:Body>
    </soap:Envelope>"""