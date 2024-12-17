import networkx as nx
import matplotlib.pyplot as plt

routes = {
    "Red":[East Port-Thampanoor -Ayurveda College - Statue- VJT 
           -Kerala University -Palayam- Niyamasabha - PMG- LMS 
           - Museum- Kanakakunnu -Manaveeyam Road -Police Headquarters-
           Vazhuthacad-Police Training College- Mettukada - Thycaud Hospital - Flyover - Thampanoor],
    "Blue":[Thampanoor-Ayurveda College - Uppiddamoodu Bridge - 
            Vanchiyoor Court - Pattoor-General Hospital -Kerala University -
              Palayam-Niyamasabha-PMG- Museum- Vellayambalam-Sasthamangalam-
              Maruthankuzhy-Kochar Road-Edapazhinji-Jagathy-Vazhuthakkad- Bakery Jn - Jacobs Jn. - Contonment Gate- Statue-Thampanoor],
    "Brown":[Thampanoor Chenthitta - Kannettumukku - Jagathy - Pangode Market - Sasthamangalam - Maruthankuzhi - PTP Nagar - Vettamukku -
             Elippodu - Valiyavila - Thirumala - Poojapura -Kunchalummoodu - Karamana - Killipalam- Attakulangara Road],
    "Green":[Transport Bhavan- Vazhapally - Fort Hospital - Uppidamoodu Bridge - Pettah Pallimukku - Kannamoola - Kumarapuram - Medical College -
             Murinjapalam -Pottakuzhy - Thekkumoodu -Anadiyil Hospital -Law College Jn - Vikas Bhavan Depot - PMG- Niyamasabha - Palayam -Statue -],
    "Majenta":[Peroorkada Depot -Ambalamukku - Kowdiar - TTC - Vellayambalam - Museum - LMS - Palayam - Statue 
               - Thampanoor-Aristo - Model School - Bakery - Palayam -Niyamasabha - PMG - Plammoodu - Pattom -
               Kesavadasapuram - Pattom -Kuravankonam - Kowdiar - Ambalamukku -Peroorkada Depot],
    "Yellow":[Peroorkada Depot - Ambalamukku - Kowdiar - TTC - Devaswom Board - Nanthancode - Museum - LMS - Palayam - VJT - Kerala University - Flyover -
              Niyamasabha - PMG - Plammoodu - Pattom - Pottakuzhy - Medical College - Ulloor - Kesavadasapuram -
              Paruthipara - Muttada - Vayalikada - Santhwana Jn. -Ambalamukku Peroorkada Depot],
    "Violet":[Peroorkada Depot - Oolampara - HLL - Paippinmoodu - Sasthamangalam - Edapazhanji - Cotton Hill School - Vazhuthacaud - Mettukada - Thycaud - 
              Thampanoor - Ayurveda College - Statue - Palayam - Niyamasabha - LMS - Museum - Vellayambalam - TTC- Kowdiar - Ambalamukku - Peroorkada Depot]
}