import osmnx as ox
import pygrib
import requests
from datetime import datetime, timezone

def coord_lister(geom):
    coords = list(geom.exterior.coords)
    return coords
def regionPolygon(address):
    if address.find("Attitash") !=-1:
        return [(-71.0001734, 42.8554006), (-71.0000517, 42.8553935), (-70.9999152, 42.8553881), (-70.9998203, 42.8553067), (-70.9997844, 42.8551914), (-70.9996413, 42.8551784), (-70.9994978, 42.8551962), (-70.9994317, 42.855234), (-70.9993027, 42.8552162), (-70.9992189, 42.8552009), (-70.999098, 42.8551985), (-70.9989867, 42.8551713), (-70.9988319, 42.8551122), (-70.9988094, 42.8550366), (-70.9987481, 42.8550543), (-70.9986852, 42.8550791), (-70.9986288, 42.8550354), (-70.9985637, 42.8549803), (-70.9984143, 42.8549799), (-70.9983337, 42.8549468), (-70.9982837, 42.8548735), (-70.9982225, 
        42.8547435), (-70.9982064, 42.8546477), (-70.9982547, 42.8545685), (-70.9981419, 42.8545437), (-70.9981096, 42.8544988), (-70.9981273, 42.8544621), (-70.9981515, 42.8544326), (-70.9981306, 42.8543404), (-70.9979548, 42.8542933), (-70.9976888, 42.8541867), (-70.9975292, 42.8541489), (-70.9974647, 42.8541135), (-70.9974159, 42.8540566), (-70.9974373, 42.853961), (-70.9976614, 42.853552), (-70.9974115, 42.8538404), (-70.9973163, 42.8539196), (-70.9972486, 42.8538972), (-70.9971922, 42.8538274), (-70.9971003, 42.8537352), (-70.9970068, 42.8536489), (-70.9967762, 42.8535875), (-70.9966762, 42.8535295), (-70.9965698, 42.8536005), (-70.9964618, 42.853643), (-70.9962683, 42.8536513), (-70.9961523, 42.8536012), (-70.99612, 42.8535213), (-70.995991, 42.853461), (-70.9958701, 42.8534527), (-70.9956443, 42.8534113), (-70.9954605, 42.8534208), (-70.9953299, 42.8533818), 
        (-70.9952396, 42.8533215), (-70.9952203, 42.8532553), (-70.9952364, 42.8531643), (-70.9952896, 42.8531229), (-70.9954202, 42.8530355), (-70.9956637, 42.8528499), (-70.9958088, 42.8527636), (-70.9958507, 42.8527199), (-70.9958975, 42.8526726), (-70.9960168, 42.8525579), (-70.9963651, 42.8523416), (-70.9964602, 42.8522731), (-70.9959781, 42.8525107), (-70.995862, 42.8525615), (-70.9956556, 42.8527329), (-70.9952525, 42.8529776), (-70.9950703, 42.853052), (-70.994943, 42.8530414), (-70.9948398, 42.8530177), (-70.9947656, 42.8530071), (-70.9946366, 42.8530378), (-70.9944641, 42.8530426), (-70.9942045, 42.8530402), (-70.9940675, 42.8529941), (-70.9939465, 42.8529102), (-70.9938869, 42.8528381), (-70.9938658, 42.8527228), (-70.9942432, 42.852214), (-70.9946947, 42.8518263), (-70.994174, 42.8521107), (-70.9936789, 42.8524693), (-70.9935322, 42.8525414), (-70.9934016, 42.8525532), (-70.9932389, 42.852541), (-70.9931275, 42.8524705), (-70.9930291, 42.8522707), (-70.9928356, 42.8521549), (-70.9926539, 42.8519249), (-70.9926696, 42.8518062), (-70.9927631, 42.8517199), (-70.9928421, 42.8516773), (-70.9929179, 42.8516738), (-70.9930162, 42.8516986), (-70.9931065, 42.851688), (-70.9931113, 42.8516608), (-70.993063, 42.851617), (-70.9930146, 42.8515851), (-70.992984, 42.8515177), (-70.9930017, 42.8514977), (-70.9931001, 42.8514811), (-70.9932049, 42.8514823), (-70.9933467, 42.851487), (-70.9934854, 42.851461), (-70.9935773, 42.8514078), (-70.9936112, 42.8512352), (-70.9935467, 42.8512317), (-70.993487, 42.8513357), (-70.9934096, 42.8514125), (-70.9931533, 42.8513877), (-70.9930013, 42.851371), (-70.992926, 42.8513628), (-70.9927163, 42.8514114), (-70.9925491, 42.8513889), (-70.9923204, 42.8514621), (-70.9921273, 42.8515076), 
        (-70.9918901, 42.8515009), (-70.9916097, 42.851409), (-70.9914136, 42.8512703), (-70.9911741, 42.8510329), (-70.9907879, 42.8509269), (-70.9902793, 42.8507268), (-70.9902531, 42.8507017), (-70.9902485, 42.8506391), (-70.990244, 42.8505764), (-70.9902508, 42.8505028), (-70.9902337, 42.8504451), (-70.9902075, 42.8504142), (-70.9901573, 42.8504025), (-70.9900319, 42.8503866), (-70.9899351, 42.8503795), (-70.9898763, 42.8503576), (-70.9898706, 42.8503257), (-70.9897973, 42.8503192), (-70.9897457, 42.8503523), (-70.9897158, 42.8504126), (-70.9896659, 42.8504587), (-70.9896046, 42.8504752), (-70.9895167, 42.8504433), (-70.989453, 42.8504321), (-70.9893539, 42.850428), (-70.9892313, 42.8504093), (-70.9891346, 42.8503833), 
        (-70.9890943, 42.8503413), (-70.9889693, 42.8502663), (-70.9888992, 42.8502503), (-70.9887936, 42.8502196), (-70.9886823, 42.8501965), (-70.9884921, 42.8502373), (-70.9884058, 42.8502615), (-70.988359, 42.8503159), (-70.9883341, 42.8503596), (-70.9882913, 42.8504075), (-70.9882881, 42.8504507), (-70.9882881, 42.8505393), (-70.9882986, 42.850641), (-70.9882526, 42.8507757), (-70.9882155, 42.8509182), (-70.9882091, 42.8510204), (-70.9881873, 42.85106), (-70.9881575, 42.8510724), (-70.9881293, 42.8510706), (-70.9881011, 42.8510582), (-70.9880833, 42.8510375), (-70.988043, 42.8508939), (-70.9880253, 42.8507816), (-70.9880084, 42.8505375), (-70.9879947, 42.850242), (-70.9879882, 42.849995), (-70.987985, 42.8498342), (-70.9879543, 42.8497621), (-70.9878923, 42.8494778), (-70.9878455, 42.8492633), (-70.9878205, 42.8491226), (-70.9878141, 42.8489926), (-70.9878181, 
        42.8489063), (-70.987831, 42.8488578), (-70.9878536, 42.8488365), (-70.987881, 42.8488241), (-70.9879092, 42.8487561), (-70.9879584, 42.8486084), (-70.987981, 42.8484074), (-70.9879818, 42.8482041), (-70.9879882, 42.8479807), (-70.9879544, 42.8477282), (-70.9879322, 42.8474837), (-70.9879161, 42.8472946), (-70.987937, 42.8471646), (-70.9879556, 42.8470605), (-70.9879507, 42.8469506), (-70.9879112, 42.8468217), (-70.9878553, 42.8466784), (-70.9877726, 42.8465302), (-70.9877173, 42.8464163), (-70.9876127, 42.8462185), (-70.9874821, 42.8460116), (-70.9873033, 42.8458), (-70.9870974, 42.8455908), (-70.9869343, 42.8453777), (-70.9868841, 42.8453095), (-70.9868099, 42.8452015), (-70.9867388, 42.8451141), (-70.9867252, 42.8450313), (-70.9866991, 42.8448673), (-70.9867012, 42.8446833), (-70.9866681, 42.8445397), (-70.9865916, 42.8443389), (-70.9865665, 42.8442435), 
        (-70.9865606, 42.8441872), (-70.9865288, 42.8441178), (-70.986426, 42.8439829), (-70.9863299, 42.843869), (-70.9861642, 42.8437575), (-70.9859698, 42.8434985), (-70.9858109, 42.8433575), (-70.985558, 42.8432386), (-70.9854777, 42.8432008), (-70.9853969, 42.8431628), (-70.9853396, 42.8431335), (-70.9853003, 42.8431134), (-70.9851583, 42.8430482), (-70.9849114, 42.8429658), (-70.9848266, 42.842941), (-70.984717, 42.8429089), (-70.9843873, 42.842826), (-70.9842067, 42.8427852), (-70.9837642, 42.8427393), (-70.9835661, 42.8427052), (-70.9832438, 42.8426786), (-70.9829984, 42.8426743), (-70.9826414, 42.842673), (-70.9824056, 42.8426927), (-70.9820772, 42.8427305), (-70.9820425, 42.8427752), (-70.9820075, 42.8427769), (-70.9818884, 42.8428001), (-70.9817725, 42.8428307), (-70.9813773, 42.8429154), (-70.981198, 42.8429745), (-70.9809628, 42.8430786), (-70.980837, 42.843154), (-70.9808081, 42.8432224), (-70.980822, 42.8433185), (-70.9808238, 42.843416), (-70.9808106, 42.8434857), (-70.9807347, 42.8436392), (-70.9806198, 42.8438408), (-70.9805513, 42.8439868), (-70.9805386, 42.8441412), (-70.9805085, 42.8442802), (-70.980523, 42.8442947), (-70.980538, 42.8443463), (-70.9805392, 42.8445563), (-70.9805115, 42.8446242), (-70.9804664, 42.8446975), (-70.980393, 42.8447535), (-70.9802757, 42.8448355), (-70.9801214, 42.8448754), (-70.9799189, 42.8449091), (-70.9797691, 42.8449159), (-70.9796866, 42.8448779), (-70.9795896, 42.8448579), (-70.9795147, 42.8448061), (-70.9794152, 42.8447251), (-70.9792603, 42.8446926), (-70.979097, 42.8446583), (-70.9789149, 42.8446022), (-70.9787371, 42.8445348), (-70.9786137, 42.844468), (-70.9783491, 42.8443501), (-70.9781526, 42.8443027), (-70.9779662, 42.8442684), (-70.9778284, 42.8442503), (-70.9776182, 42.8442572), (-70.9774302, 42.8442447), (-70.9772405, 42.8442173), (-70.9769614, 42.8441967), (-70.9767155, 42.8442098), (-70.9764016, 42.844284), (-70.9761285, 42.8443526), (-70.9759004, 42.8443901), (-70.9757941, 42.8443919), (-70.9754912, 42.8443844), (-70.9751721, 42.8443533), (-70.9750734, 42.8443345), (-70.9749297, 42.8442815), (-70.9748403, 42.844269), (-70.9747323, 42.8442653), (-70.9746191, 42.8442803), (-70.974523, 42.8442984), (-70.974426, 42.8443171), (-70.9742595, 42.8443706), (-70.9740559, 42.8444543), (-70.9738341, 42.8445932), (-70.9736335, 42.844786), (-70.9733327, 42.8450325), (-70.9729062, 42.8454559), (-70.9727126, 42.845603), (-70.9725502, 42.845776), (-70.9722739, 42.8461653), (-70.9720252, 42.8465821), (-70.9717711, 42.8470517), (-70.9714957, 42.8475797), (-70.9714875, 42.8476582), (-70.9715216, 42.8477609), (-70.9715687, 42.8478584), (-70.9716358, 42.8480232), (-70.9717087, 42.8480836), (-70.9717711, 42.8480991), (-70.9718382, 42.8481302), (-70.9719088, 42.848213), (-70.9719794, 42.8483217), (-70.9720676, 42.8484563), (-70.9721359, 42.8486176), (-70.9721959, 42.8487065), (-70.9722818, 42.8487954), (-70.9723477, 42.8488911), (-70.9723465, 42.8489291), (-70.9724018, 42.8490646), (-70.9730259, 42.8503063), (-70.973079, 42.8503592), (-70.9731994, 42.8504185), (-70.9733544, 42.850505), (-70.973518, 42.8506263), (-70.9736952, 42.8508445), (-70.9740126, 42.8513307), (-70.9741466, 42.851453), (-70.9743714, 42.8515824), (-70.9744968, 42.8516263), (-70.9748975, 42.8518387), (-70.9753971, 42.8521039), (-70.9756342, 42.8521895), (-70.9758219, 42.8522411), (-70.9761868, 42.8523276), (-70.9766154, 42.8523991), (-70.9768012, 42.8524263), (-70.9770644, 42.852455), (-70.9770754, 42.8524361), 
        (-70.9772934, 42.8524646), (-70.9773948, 42.8524999), (-70.9780755, 42.8526561), (-70.978775, 42.8527922), (-70.9792339, 42.8529434), (-70.979466, 42.8530984), (-70.9797136, 42.8532868), (-70.9798631, 42.8534806), (-70.9799384, 42.8536218), (-70.9800066, 42.8537217), (-70.9800497, 42.8537656), (-70.9800875, 42.8538383), (-70.9800365, 42.8539357), (-70.979954, 42.8541084), (-70.9798882, 42.8541514), (-70.9799014, 42.8542268), (-70.9799026, 42.8543671), (-70.9798438, 42.8546499), (-70.979832, 42.8544881), (-70.9798595, 42.8542855), (-70.9798404, 42.8541742), (-70.9798607, 42.8541312), (-70.9798977, 42.8541076), (-70.9799156, 42.8540067), (-70.9798271, 42.8539655), (-70.9797721, 42.8539909), (-70.9797039, 42.8540093), 
        (-70.9796584, 42.8540549), (-70.9795974, 42.854126), (-70.9795879, 42.8541751), (-70.9795352, 42.8542154), (-70.9794994, 42.8542329), (-70.9794252, 42.8542338), (-70.9793355, 42.8541891), (-70.9791979, 42.8541575), (-70.9791118, 42.8541549), (-70.9790006, 42.8541733), (-70.9789133, 42.8542242), (-70.9788702, 42.8542873), (-70.9788367, 42.8543767), (-70.9788224, 42.8544905), (-70.9788561, 42.8546266), (-70.9788782, 42.8547907), (-70.9789081, 42.8549103), (-70.9789581, 42.8550323), (-70.9789539, 42.8550805), (-70.9789797, 42.8551739), (-70.9790272, 42.8553234), (-70.9791129, 
        42.8555046), (-70.9792819, 42.8556529), (-70.9794517, 42.8557548), (-70.9795674, 42.8557743), (-70.9796639, 42.8558103), (-70.9797788, 42.8558848), (-70.9799178, 42.8560227), (-70.9799078, 42.8560776), (-70.9799544, 42.856188), (-70.9799761, 42.8562753), (-70.9800077, 42.8563509), (-70.98016, 42.8565126), (-70.9802266, 42.8565535), (-70.9804397, 42.856692), (-70.9805089, 42.8567106), (-70.9809059, 42.8568219), (-70.9809886, 42.8567908), (-70.981014, 42.8567813), (-70.9811045, 42.8567167), (-70.9811422, 42.8566226), (-70.9812005, 42.8564621), (-70.9811813, 42.8564579), (-70.9811938, 42.8564133), (-70.9812313, 42.8563285), (-70.9812571, 42.8562803), (-70.9814119, 42.8561174), (-70.9814585, 42.8560875), (-70.9815551, 42.8560405), (-70.98164, 42.8560039), (-70.9817856, 42.8559679), (-70.981913, 42.8559508), (-70.982156, 42.8559612), (-70.9821852, 42.8559752), (-70.9823168, 42.8559985), (-70.9823713, 42.8560324), (-70.9826991, 42.8560766), (-70.9828752, 42.8561097), (-70.9830177, 42.8561428), (-70.9831741, 42.85617), (-70.9833282, 42.8561955), (-70.9834301, 42.8562031), (-70.9835008, 42.8561963), (-70.9836317, 42.8561862), (-70.9837719, 42.8561301), (-70.9840545, 42.8560477), (-70.9841453, 42.8560002), (-70.9841808, 42.8559543), (-70.9842028, 42.8558448), (-70.983912, 42.8552155), (-70.9838993, 42.8551475), (-70.9838842, 42.855021), (-70.9838622, 42.8548817), (-70.9838703, 42.8548299), (-70.9839062, 42.8547136), (-70.9839456, 42.8546465), (-70.9839781, 42.8545599), (-70.9841565, 42.8543009), (-70.9841924, 42.8542711), (-70.9843291, 42.8541964), (-70.9844102, 42.8541786), (-70.9844681, 42.8541667), (-70.9845318, 42.8541667), (-70.9846245, 42.8541879), (-70.9847322, 42.854227), (-70.9849338, 42.8543238), (-70.985166, 
        42.8544191), (-70.9853311, 42.8544673), (-70.9854725, 42.8544817), (-70.9856833, 42.8544716), (-70.9860904, 42.8544438), (-70.9865378, 42.8544343), (-70.9866595, 42.854432), (-70.986795, 42.8544154), (-70.9869498, 42.8543829), (-70.9870925, 42.8543339), (-70.9872064, 42.8542775), (-70.9873077, 42.8542222), (-70.9873964, 42.8541849), (-70.9874407, 42.8541524), (-70.987506, 42.8541052), (-70.9875987, 42.8540815), (-70.9877076, 42.8540679), (-70.9877839, 42.8540731), (-70.9878446, 42.8540981), (-70.9878672, 42.8541288), (-70.9878833, 42.8541548), (-70.987864, 42.8541914), (-70.9878092, 42.8542281), (-70.9877963, 42.8543155), (-70.9878027, 42.8543451), (-70.9878785, 42.8543865), (-70.9879704, 42.8543959), (-70.9880591, 
        42.8544231), (-70.9881268, 42.8544385), (-70.9882364, 42.8544928), (-70.9883396, 42.8545153), (-70.9885137, 42.8545165), (-70.9886073, 42.8545153), (-70.9887927, 42.8544586), (-70.9889555, 42.8543841), (-70.9890781, 42.8542884), (-70.9891345, 42.8542364), (-70.98917, 42.8541773), (-70.9891361, 42.8541382), (-70.9891168, 42.8540815), (-70.9891152, 42.853994), (-70.989149, 42.8539101), (-70.989228, 42.8537896), (-70.989336, 42.8536832), (-70.9894279, 42.8535614), (-70.9895279, 42.8533652), (-70.9895473, 42.8532766), (-70.9895795, 42.8531584), (-70.9896408, 42.8531217), (-70.989694, 42.8530874), (-70.9897407, 42.8530898), (-70.9897891, 42.853104), (-70.9898375, 42.8531395), (-70.989831, 42.8531808), (-70.9898439, 42.8532187), (-70.9899552, 42.8532187), (-70.9900803, 42.8531901), (-70.9902003, 42.8531584), (-70.9903164, 42.853065), (-70.9904615, 42.8528924), (-70.9907917, 42.8523214), (-70.9908328, 42.8522853), (-70.9909182, 42.8522593), (-70.9909892, 42.8522563), (-70.9910593, 42.8522758), (-70.9910779, 42.8523078), (-70.9911069, 42.8523568), (-70.9911827, 42.8523698), (-70.9912359, 42.8523485), (-70.9913004, 42.8523072), (-70.9914124, 42.8523137), (-70.9914213, 42.8523609), (-70.9914793, 42.8524065), (-70.9917321, 42.8525), (-70.9917881, 42.8525276), (-70.9918397, 42.8525625), (-70.9920445, 42.8526174), (-70.9920292, 42.85267), (-70.992084, 42.8527067), (-70.992163, 42.8527274), (-70.9921573, 42.8527699), (-70.9921928, 42.8528166), (-70.9922275, 42.8528828), (-70.9922742, 42.852881), (-70.9922944, 42.852939), (-70.9922976, 42.8529839), (-70.9923428, 42.8530483), (-70.9923927, 42.8531216), (-70.9923831, 42.8531712), (-70.9923605, 42.8532209), (-70.9923855, 42.8532528), (-70.9924016, 42.8532936), (-70.9923782, 42.853329), (-70.9923758, 42.8534313), (-70.9923226, 42.8534856), (-70.9922718, 42.853498), (-70.9922629, 42.8535294), (-70.9922613, 42.8535737), (-70.9922347, 42.8535902), (-70.9922162, 42.8536204), (-70.9922202, 42.8536901), (-70.9922218, 42.8537256), (-70.9922847, 42.8537474), (-70.9923895, 42.8537575), (-70.992475, 42.8537504), (-70.9925346, 42.8537108), (-70.9925943, 42.8536807), (-70.9926628, 42.8536612), (-70.9927467, 42.8536568), (-70.9927926, 42.8536635), (-70.9927958, 42.8536996), (-70.9927128, 42.8537398), (-70.9926676, 42.8537746), (-70.9927483, 42.853761), (-70.9927734, 42.8537504), (-70.9929102, 42.8536685), (-70.9930196, 42.8535465), (-70.9931054, 42.8534124), (-70.9931633, 42.8533893), (-70.993234, 42.8533743), (-70.9933571, 42.8534311), (-70.9935714, 42.8535013), (-70.9938633, 42.8536033), (-70.9940982, 42.8536451), (-70.9942578, 42.8536384), (-70.9944539, 42.8536233), (-70.994634, 42.8536434), (-70.9948803, 42.8537287), (-70.9950285, 42.8538306), (-70.9951744, 42.8538925), (-70.9953272, 42.8538774), (-70.9955415, 42.8538891), (-70.9957604, 42.8539727), (-70.9959781, 42.854079), (-70.9960825, 42.8541061), (-70.9962296, 42.8541442), (-70.9963763, 42.8541619), (-70.9964618, 42.8541702), (-70.9964989, 42.854117), (-70.996615, 42.8540449), (-70.9967133, 42.854), (-70.9968052, 42.8540496), (-70.9968794, 42.8541773), (-70.99701, 42.8542978), (-70.9971019, 42.8543971), (-70.9971112, 42.8544846), (-70.9972325, 42.8545272), (-70.9974002, 42.8545071), (-70.9975324, 42.8545732), (-70.9976049, 42.8546761), (-70.9976162, 42.8547754), (-70.9976985, 42.854812), (-70.9977807, 42.8548841), (-70.9978452, 42.8549361), (-70.9978855, 42.8550319), (-70.9979677, 42.8550874), (-70.9979812, 42.8551257), (-70.9980225, 42.8551737), (-70.9980145, 42.8552978), (-70.9981144, 42.8552434), (-70.9982015, 42.8552162), (-70.9982644, 42.8552352), (-70.9982837, 42.8552943), (-70.9983821, 42.8551914), (-70.9984418, 42.8551962), (-70.998532, 42.8552021), (-70.9987723, 42.8552576), (-70.9988642, 42.8553037), (-70.9989722, 42.8553474), (-70.9991044, 42.8553049), (-70.999256, 42.8553474), (-70.9994785, 42.8553522), (-70.9995994, 42.8553734), (-70.9996623, 42.8553841), (-70.9997332, 42.8553758), (-70.999855, 42.8554325), (-70.9998759, 42.8555111), (-70.9999388, 42.8555035), (-71.0000202, 42.8554568), (-71.0001734, 42.8554006)]
    elif address.find("Shoreline") !=-1:
        return [(-122.0955957, 37.4340436), (-122.0955877, 37.4340228), (-122.0955924, 37.4339753), (-122.0955512, 37.4338858), (-122.0955557, 37.4338538), (-122.0955168, 37.433777), (-122.0954919, 37.4336964), (-122.0954814, 37.4335824), (-122.0954936, 37.4334744), (-122.0954667, 37.4333602), (-122.0954692, 37.433312), (-122.0954448, 37.4332734), (-122.0954049, 37.4332387), (-122.0952902, 37.4331948), (-122.0951185, 37.4330614), (-122.0949561, 37.4329145), (-122.0948404, 37.4327762), (-122.0947764, 37.4326541), (-122.0947575, 37.4325474), (-122.0947608, 37.4325036), (-122.0947447, 37.4324594), (-122.0946951, 37.4323664), (-122.0946746, 37.4323465), (-122.0945922, 37.4322913), (-122.0943162, 37.4321905), (-122.0940917, 37.4320485), (-122.0940366, 37.4320253), (-122.0939721, 37.4320188), (-122.0939134, 37.4320204), (-122.0937417, 37.4320524), (-122.0935564, 37.4320978), (-122.0933314, 37.4321799), (-122.0933023, 37.432219), (-122.0932693, 37.432226), (-122.0932519, 37.4322423), (-122.0931047, 37.4321894), (-122.0929428, 37.4319487), (-122.0928735, 37.4317211), (-122.0928621, 37.4315865), (-122.092827, 37.4315056), (-122.0925288, 37.4311679), (-122.0923642, 37.4310187), (-122.0922979, 37.430778), (-122.0922647, 37.4307066), (-122.0922326, 37.4306663), (-122.0919986, 37.4305156), (-122.0914983, 37.4302638), (-122.0914175, 37.4302556), (-122.0912818, 37.4302772), (-122.0911153, 37.4303269), (-122.0910432, 37.4303697), (-122.0909387, 37.4305011), (-122.0905499, 37.4310481), (-122.0904777, 37.431126), (-122.0904174, 37.4311728), (-122.0902557, 37.4312409), (-122.0899823, 37.4313207), (-122.0898613, 37.4313644), (-122.0896356, 37.4314188), (-122.0893952, 37.4314578), (-122.0890123, 37.4314628), (-122.0888902, 37.4314784), (-122.0888394, 37.4314946), (-122.0887552, 37.4315502), (-122.088651, 37.4316613), (-122.0885929, 37.4317456), (-122.0885669, 37.4318302), (-122.0885641, 37.4319212), (-122.0886115, 37.4321232), (-122.0886102, 37.4322027), (-122.0885583, 37.4324076), (-122.088453, 37.4327169), (-122.0884113, 37.4327944), (-122.0883621, 37.4328486), (-122.0882415, 37.4329473), (-122.0883475, 37.4329809), (-122.0883326, 37.433008), (-122.0881062, 37.4329251), 
        (-122.0880704, 37.4329909), (-122.0880915, 37.432999), (-122.0879791, 37.4332064), (-122.0879366, 37.4333865), (-122.0879531, 37.4335413), (-122.0879926, 37.4336352), (-122.0880868, 37.4337323), (-122.0882384, 37.4337979), (-122.0888893, 37.4340477), (-122.0891157, 37.4341115), (-122.0893062, 37.4341292), (-122.0894213, 37.4341218), (-122.089478, 37.4341077), (-122.0895934, 37.4340464), (-122.0897393, 37.4339299), (-122.0899964, 37.4336894), (-122.090032, 37.4336676), (-122.090096, 37.4336448), (-122.0901112, 37.4336472), (-122.0901309, 37.4336538), (-122.0902199, 37.4337262), (-122.0902986, 37.4338207), (-122.0903178, 37.4338679), (-122.0903702, 37.4339445), (-122.0904214, 37.434128), (-122.0904682, 37.4342158), (-122.0905343, 37.4342879), (-122.0906155, 37.4343412), (-122.0907647, 37.4344064), (-122.0908671, 37.434424), (-122.0909841, 37.4344319), (-122.0912239, 37.4344113), (-122.0914545, 37.4343589), (-122.0916992, 37.434256), (-122.092128, 37.4341045), (-122.0922512, 37.4340726), (-122.0924498, 
        37.4340792), (-122.0927024, 37.4341242), (-122.0928198, 37.4341622), (-122.0931046, 37.4342954), (-122.0937552, 37.4346688), (-122.0938298, 37.4346946), (-122.0939008, 37.4347071), (-122.0940381, 37.4346991), (-122.0941632, 37.4346666), (-122.0942928, 37.4346285), (-122.0947345, 37.4344614), (-122.0948048, 37.4344453), (-122.0948449, 37.4344411), (-122.0949518, 37.4344849), (-122.095102, 37.4345915), (-122.0951495, 37.4346057), (-122.0952451, 37.4345903), (-122.0952825, 37.434571), (-122.0953391, 37.4344901), (-122.0953743, 37.4344631), (-122.095449, 37.4343911), (-122.0954385, 37.4343237), (-122.0954502, 37.4342847), (-122.095557, 37.434145), (-122.0955619, 37.4340792), (-122.0955957, 37.4340436)]
    else:
        print("Fetching cords ... ")
        area = ox.geocode_to_gdf(address)
        cords = area.geometry.apply(coord_lister)[0]
        return cords



def downloadGrib(name):
    day = datetime.now(timezone.utc).strftime('%Y%m%d')
    #GRIB_URL="http://nomad.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs."+ time + "/gfs.t00z.pgrbf"+str(forcast)+".grib2"
    #vlmgrib = "http://grib.v-l-m.org/latest.grb"
    forcast = 10
    hour = datetime.now(timezone.utc).strftime('%H')
    url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/rap/prod/rap."+day+"/rap.t"+hour+"z.wrfprsf"+str(forcast)+".grib2"
    response = requests.get(url)
    if response.status_code != 200:
        while response.status_code != 200 and int(hour)>=0:
            hour = str(int(hour)-1).rjust(2, '0')
            print("fetching earlier::", hour)
            url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/rap/prod/rap."+day+"/rap.t"+hour+"z.wrfprsf"+str(forcast)+".grib2"
            response = requests.get(url)
        if int(hour) <0:
            print(f"{response.status_code} error when fetching latest GRIB")
            return 0
    
    with open(name + ".grib2","w+", encoding="utf-8") as save:
        save.write(response.text)
    print(response)

def loadGrib(file):
    grib = pygrib.open(file)
    #print(dir(grib),grib.read(1))
    grib.seek(1)
    print(grib.tell())
    # for g in grib:
    #     print(g)


#loadGrib("test.grib2")
#print(datetime.now(timezone.utc).strftime('%H'))
downloadGrib("test")
#downloadGrib(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S'))