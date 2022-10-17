import pandas as pd
import numpy as np
from re import search
from datetime import datetime
pd.set_option('mode.chained_assignment', None)


from functions.homogenization_functions import absorption_efficiency, stoichmetry_conversion, conversion_efficiency, \
    background_correction,pumptemp_corr, currenttopo3, pf_groundcorrection, calculate_cph, pumpflow_efficiency, \
    return_phipcor, o3_integrate, roc_values, RS_pressurecorrection, o3tocurrent, background_correction_3split

from functions.functions_perstation import df_missing_variable, madrid_missing_tpump, df_station, \
    station_inone, station_inbool, station_invar, df_drop


# homogenization code to be used by all stations
### all corrections recommended by the DQA:
## Conversion Efficiency:
#  absorption and stoichiometry->
#  variables:solution volume,
#  sonde type and solution concentration
## Background Current:
#  df of all metadata is needed to calculate the mean and std of bkg.
#  most of the time 2 different periods are needed
#  which has a parameter IBGsplit the year in which
#  bkg values has changed from high to low
#  which bkg is used important, mostly iB2
#  but this can be station specific
## Pump Temp. Measurement (location):
#  pump location. if a change in the type of the sonde was made
#  this would effect this variable
## Pump Flow Rate (moistening effect)
#
## Pump flow efficiency at low pressures
# TON not to be applied but to be kept in the database
# Radiosonde correction (not to be applied)

k = 273.15
roc_plevel = 10 # pressure value to obtain roc

##                                         ##
##           TO BE CHANGED By HAND         ##

station_name = 'scoresbysund'
main_rscorrection = False  #if you want to apply rs80 correction
test_ny = False
scoresbysund_tpump = True
# mm = [
#     [302.67802719279905, 301.6913167923789, 302.069148677286, 302.98619192528616, 303.9651864314356, 304.1554886438513,
#      304.4154809753607, 304.2719898285388, 302.757597475935, 302.654979957836, 301.7678875812494, 302.2626288997596],
#     [302.1901418262213, 301.3736762332204, 301.65317461573056, 302.26733106094645, 303.85883634366087, 303.995139160152,
#      304.5332286945626, 304.1560950058813, 302.5516876550159, 302.37316658425965, 301.52588338542347,
#      302.5436132488726],
#     [301.79031449399815, 301.03346888215646, 301.1667512601403, 301.80097090054505, 303.9551956448694,
#      303.7915094432767, 304.46525551873657, 303.91153559161086, 302.6034601869576, 301.96775354421175,
#      301.24611133888834, 302.59428235387946],
#     [301.3756969859505, 300.60010731767244, 300.5042652033912, 301.6728204381174, 303.8531363376103, 303.57270902777793,
#      304.2819049741156, 303.5902594981537, 302.6245454082374, 301.2916429888187, 300.8169533183608, 302.36338013779505],
#     [300.9380265925685, 300.07638250426714, 299.8356564911566, 301.3034772224167, 303.6208806990852, 303.12522649315514,
#      304.05414215302926, 303.2065131639101, 302.5958523136712, 301.01852623081186, 300.3036030331118,
#      301.8569772699803],
#     [300.3685514093873, 299.54578530201115, 299.13801771141243, 300.46301913862345, 303.4143592346499,
#      302.76637196370075, 303.7044262557398, 302.71676418291725, 302.19992332162633, 300.7770777221587,
#      299.7812795013316, 301.2523572400754],
#     [299.78510682017736, 298.82560185155006, 298.56125627368823, 300.3255369657643, 303.06787126289777,
#      302.25681751028105, 303.2941877611057, 302.1959476193702, 301.552925585328, 300.2444474589163, 299.24774638014935,
#      300.62662637853657],
#     [299.08319001311384, 298.0526729352169, 298.85486235094567, 299.97742612603093, 302.64316403584627,
#      301.70762914878696, 302.8321143229121, 301.56941161730265, 300.5993338164294, 299.9738219193435,
#      298.55318643858584, 299.9912861111476],
#     [298.3297678853345, 297.319040678579, 298.7165426002716, 299.48037600474413, 302.0006534761711, 301.0611854178675,
#      302.1450852771687, 300.7815251357494, 299.7283792001857, 300.176454268171, 297.67753537210643, 299.27614967790385],
#     [297.6026589137431, 296.979435189855, 297.9918905484531, 298.8715151431416, 301.4988431285972, 300.544718957037,
#      301.3523934919348, 299.9079844631564, 298.8499192058206, 297.9716248364121, 297.0612337055241, 298.5949804553936],
#     [297.02878883443447, 296.1297964772637, 297.1827620570913, 298.3636115708994, 300.492684317543, 299.81361064901887,
#      300.35204116217636, 298.8649629682858, 299.3715607280974, 297.19358460762686, 296.72414455540036,
#      297.9174597900953],
#     [296.4399004516917, 296.3467762881832, 296.2787750159961, 297.4502901863707, 299.4647174890848, 298.99865789238237,
#      299.42839513488775, 297.8166844187547, 298.99726264839495, 297.5589362475123, 295.95380912627706,
#      297.1896535638639],
#     [295.3102019709912, 295.76860843799625, 295.3827372862911, 296.59866156285943, 298.59394105851516,
#      298.9718013509053, 298.70958374351903, 296.83549367870376, 298.1347602953581, 296.94626675003735,
#      296.2747344782187, 296.8419235862288],
#     [294.5133692208688, 295.25155693007093, 294.82037440850587, 295.9529877809352, 298.86140084781, 299.1155457731957,
#      298.0987829489465, 296.00820523503404, 298.23723489345946, 296.4674763795148, 296.1221767789067,
#      296.12506020120645],
#     [293.8396710811117, 294.7263101322812, 294.98226283568437, 296.0965515712661, 298.5182087530858, 298.2559091914825,
#      297.5382946582131, 296.1297255385673, 298.1441871154078, 295.92738898536584, 296.1192031618715,
#      295.38074711250994],
#     [293.07793477997, 294.2327455126112, 294.99435832243745, 297.223823441037, 299.3166961911547, 297.5454922165541,
#      299.0798493072854, 297.83328037180905, 298.0689602145941, 295.69604206543926, 296.07252332822736,
#      295.0436945536848],
#     [292.3945383747964, 293.65685867028435, 295.434906148884, 298.34101787606187, 299.19703046429015, 297.1975917165747,
#      298.9314896550023, 296.1229541896948, 298.0224094348738, 297.2416403107661, 295.68994584615984, 295.2880394681437],
#     [291.91906442437954, 292.5711539431071, 294.96358263408973, 299.16874803658214, 299.1947201708061,
#      297.37618854497157, 299.2169816690833, 296.08373418802364, 298.14807649742954, 297.42998764355127,
#      295.0559539129313, 294.66637570505736],
#     [291.7632335748525, 291.6949051575771, 294.5309311406554, 299.9302318439871, 298.8376746825994, 297.46246218587555,
#      299.2055414135458, 296.50298123169097, 297.8118395255115, 296.9284332004105, 294.4318245630922, 294.1082852741565],
#     [291.66417669801655, 290.56677473709163, 294.0689182414437, 299.92285707960013, 298.5153073375675,
#      297.88032230416525, 298.95673091497224, 296.6349034565058, 298.157712719812, 296.43301725205214, 293.7705704982974,
#      293.5789567514298],
#     [290.91480890971326, 290.34726936400364, 294.4731123138731, 299.86616718603085, 298.489341461808,
#      298.05859171180646, 299.19187130699584, 296.89912946641977, 297.81158718973643, 296.08818584631325,
#      293.1523605655649, 292.98094393486247],
#     [290.57186111495884, 290.28780264228226, 294.6667338863203, 299.50580449489433, 298.3584065691036,
#      297.7991486130869, 299.50252346507006, 295.95134073782936, 297.56633285578255, 295.7437850845953,
#      292.66803450254145, 293.0233050127733],
#     [290.4379801059582, 290.294394554214, 295.0975509944922, 299.3810486850044, 298.31054434430024, 297.5380355784229,
#      299.0662531072352, 295.36322449962046, 297.2202533763016, 295.5865291993131, 294.6447747467261, 292.564254195794],
#     [290.36490497007117, 290.2270435900509, 294.417366634178, 299.19956955990256, 298.22894206329835, 297.3520688575495,
#      298.65649847971133, 295.2319704637537, 297.0753234755348, 295.48155799159815, 293.9923691365993,
#      292.2260984576568],
#     [289.6177302684849, 290.096958227369, 294.0750568548661, 298.7940436922659, 297.7555718630563, 297.1544498963254,
#      298.21961662397456, 295.10025628381374, 296.5763455221966, 294.7609466811333, 293.5178924894664,
#      292.0256903395887],
#     [289.97007764406, 289.9050056070334, 293.6697640969583, 298.32121837736696, 297.56486551231285, 297.0061312430069,
#      297.75906393357843, 295.0181514083005, 295.8675888436954, 294.5115240247843, 292.16083813546214,
#      291.47841453223225],
#     [288.80943467219026, 290.3783967922958, 293.3875956108574, 297.2941578466943, 297.3238228566148, 296.8320410443095,
#      297.359728781703, 294.7622011547205, 295.30945892218756, 294.2935220105162, 291.90109001569795, 291.2118346726467],
#     [287.9231354795931, 290.18711736410955, 292.75962980511287, 296.61224878254444, 297.25610110633227,
#      296.75808136409387, 296.9857095877503, 294.12347438623465, 294.5660488237275, 294.00326158166814,
#      290.87324751382084, 290.5756339970811],
#     [287.7375737735912, 290.8840039633573, 292.17367670239, 296.0352708711363, 297.1614253675134, 296.60799189347244,
#      295.8325671627085, 293.5264773378307, 293.62790066268207, 293.0515996274556, 290.074946381701, 289.95198381741716],
#     [287.7198015314537, 290.83474842294765, 291.83611744794695, 295.47508260438724, 296.8837323582054,
#      295.41837827640296, 296.51412176927334, 293.0173556342777, 293.1835793450927, 292.4930236215263, 289.4033711493214,
#      289.3422418381051],
#     [288.7871572432218, 289.4322242033048, 289.9646885422413, 294.82770386370237, 296.3459983370697, 295.2083842990983,
#      296.4191198581217, 292.52009048613473, 292.68238662990655, 292.1622859462267, 291.47541668986025,
#      290.04688308054574],
#     [287.35860469564227, 290.2198840988319, 289.7277349172332, 293.9190973915886, 293.9811628801665, 294.7597558171958,
#      295.50768629408395, 292.0994552659016, 292.49156559571753, 291.71208554233493, 291.329454416472,
#      293.4113385956312],
#     [287.31886647248416, 289.73848586179065, 289.60559209682367, 293.1106120019374, 293.33364829784364,
#      293.48133610145396, 293.07778751185197, 290.8848610536458, 292.25717122360004, 291.3874615702568,
#      291.3289875216094, 292.48914015783936],
#     [287.53206761987246, 288.6217361319913, 290.3402820067437, 294.44502091740077, 293.08660465166275,
#      292.4558774809533, 291.49534912617537, 291.5973003996537, 288.67712539837527, 289.48489243398626,
#      288.9429397288499, 290.4554146154346],
#     [289.1281866536855, 288.1961744646036, 289.7683520069376, 291.8737645404391, 292.0113387777477, 292.6142336190799,
#      294.9900098655726, 291.6173826111121, 289.6629863256803, 289.44322523553626, 286.24535719924785,
#      289.84257878139266]]

mm = [
    [299.0699499530646, 299.0396648077781, 300.7441395179778, 302.91768667398304, 303.76893536201874, 303.4633444777978,
     303.3841414303539, 303.76734537554677, 302.53460978843367, 301.36535384274106, 299.54102687658406, 300.8928456137918],
    [298.0985387108544, 298.09570963066983, 299.82167916633915, 302.47809142310643, 303.47331800922746, 303.1988036671704, 302.85474450359516, 303.54350299639333, 302.37412718156037, 300.69720329472807, 298.5883574042559, 299.86222363763716],
    [297.01118392620634, 297.23596330007086, 298.9587777828401, 301.8476098502563, 303.09250765803654, 302.8526101423111, 302.82620551300226, 303.04158093693593, 301.90114488970147, 299.87638855217915, 297.6947137331075, 299.05426059091076],
    [295.88550604917555, 296.3344915505819, 298.0812411341353, 301.0735526429956, 302.67174969229046, 302.36075575912986, 302.49592079779273, 302.51093819787013, 301.1948358594081, 298.966543575754, 296.7586251870247, 298.12217077064713],
    [295.0506664093881, 295.333090453737, 297.2081051029264, 300.0379535020152, 302.1627317559172, 301.81311609802106, 302.0955569910676, 301.8028165017288, 300.5313999592352, 298.02921078730094, 295.8126273760377, 297.19372849651484],
    [293.8901527346695, 294.2878885808076, 296.30086200996766, 298.9475791316264, 301.5967466595328, 301.13442214476873, 301.3063541889061, 301.17141651352296, 299.7477220221424, 297.03706612093845, 294.90701300049204, 296.25139067515386],
    [292.82204999252974, 293.2724544735296, 295.40504359192005, 297.88188094393587, 300.83911973844215, 300.52465819357917, 301.0247762035437, 300.39764239316384, 298.8680753883205, 296.1370163180119, 293.9057725543006, 295.3576037313521],
    [291.6918502204674, 292.2317425306229, 294.49366477644514, 296.7670639173377, 300.1060009446819, 299.7085458125847, 300.4331390125351, 299.6344598870733, 297.9836178633143, 295.3594794106596, 293.0049197478418, 294.3339108545996],
    [290.5871409624118, 291.1986046352061, 293.52555555144545, 295.76289186127644, 299.33768936500405, 298.8148157499571, 299.7538740165909, 298.71071351505907, 297.06986751819903, 294.5824027261445, 292.1445300202429, 293.2786357305715], [289.50844623470846, 290.1735498745908, 292.5523300556073, 294.67084939390224, 298.4901562763059, 297.79246503561683, 298.7262234539853, 297.6424591160551, 295.96199057906705, 293.74450981027144, 291.2059793645486, 292.151868563648], [288.42915554524103, 289.2030450488843, 291.5656232861744, 293.52958700882255, 297.5600685646135, 296.7484088396909, 297.650439876622, 296.5234839174144, 294.75827144542075, 292.81145875191226, 290.23917377786995, 290.98346716489357], [287.3740538448776, 288.1616135366936, 290.5784107973915, 292.433921106699, 296.6079940607595, 295.7639574722658, 296.57032223895266, 295.4148917130881, 293.56932841436037, 291.84434830730555, 289.20391333419417, 289.86695078385685], [286.43501631434117, 287.16636937563715, 289.6398987687917, 291.29310031431476, 295.6640999653132, 294.8255166079915, 295.5816128700793, 294.48012441595495, 292.5114668793624, 290.8641967107459, 288.1364927527132, 288.767550188754], [285.46620813085326, 286.2236731369256, 288.76038753782757, 290.2159774051597, 294.79977917756014, 293.9995940175578, 294.6185692099591, 293.5459065612381, 291.53589999272907, 289.8769464451731, 287.16176224967586, 287.7484444998381], [284.5565062076614, 285.284107433009, 287.94609203587686, 289.3997236497099, 293.99114160216743, 293.35940078347187, 293.7791979180296, 292.7982685967161, 290.60951264442605, 288.9755827479388, 285.1481680739088, 286.7255699566439], [283.57276052510576, 284.4153969724758, 287.1752826935036, 288.65138870192663, 293.2612971536006, 292.643178405581, 293.0655927921562, 292.009165833944, 289.79956308842225, 288.0946341014806, 284.3166200928937, 285.69349793830753], [282.7406658492346, 283.640775719462, 286.46899658676807, 287.9215165168781, 292.5598607973561, 291.93621013580514, 292.3402282977021, 291.36966646041753, 288.98440426582647, 287.2840268451013, 283.5865460938841, 284.68511778491643], [282.1513560769551, 283.04839643568425, 285.8474041348161, 287.2286683563924, 291.894948992509, 291.19032569102876, 291.68506263849173, 290.7670036827596, 288.2834162138928, 286.58168052120465, 282.90804953799795, 283.68058166021035], [281.70462477720207, 282.18973428706124, 285.2414223278296, 286.6031140933371, 291.30240081250975, 290.59747501384663, 291.0932293892513, 290.2447818799768, 287.7036402224212, 286.11380253446754, 282.2871835579186, 282.60234123758613], [281.3958878586434, 281.57739164933787, 284.67381126446435, 285.9545249198576, 290.7805994516811, 290.1008673667983, 290.5513519792611, 289.7239392239103, 286.90772799972615, 285.6208895247762, 281.8725445920712, 281.61993649891764], [281.10024010799367, 281.1536151009838, 284.14029819554446, 285.589328255055, 290.30811628194624, 289.67150987125575, 290.0696493993947, 289.3667848027693, 286.31266731760013, 285.2216170852837, 281.44506927109285, 280.66150571758664], [280.55253798509534, 281.07177426752196, 283.6292831817552, 285.0197894945378, 289.80808591998357, 289.23996145740176, 289.6201964014941, 289.0230710341407, 285.8001693778451, 284.82691154566305, 280.7894942735059, 280.26451053630035], [280.2278478918897, 280.9929142254971, 283.1848708965563, 284.5192413453789, 289.35347651524114, 288.91948307944807, 289.194086276153, 288.7214170099287, 285.2877963630564, 284.4070292104233, 280.5669582110675, 280.4904063313466], [280.1707215264664, 280.76433965851186, 282.8601501580857, 284.09122010674577, 288.9386786990133, 288.71054339879083, 288.8151826774926, 288.4096485488384, 284.9155651968522, 284.0726453755962, 280.29234209942047, 280.6724823889556], [280.2323194623867, 281.02645690873044, 282.55793453589035, 283.6497366965566, 288.53564340633613, 288.52321794673855, 288.4585720910581, 288.0340183654638, 284.37671215141705, 283.82753989342126, 280.4514858753591, 280.5131077162347], [280.12350181339383, 281.1665995560709, 282.668341277622, 283.25172138214316, 288.20095646732534, 288.3108543353559, 288.12376731940714, 287.659602112164, 283.9370469329753, 283.4747916180526, 280.5095215038923, 280.8116957870873], [280.1156041123964, 281.4449696546325, 282.3926357691795, 282.8782727614083, 287.9085377269852, 288.17256221147517, 287.833359215834, 287.34890174379564, 283.5170410664108, 283.04179910213674, 280.7060149145121, 280.58780311112446], [280.2308430218324, 281.4721747170639, 282.31298147976395, 282.68247192775436, 287.6365214072298, 287.99949808702115, 287.6035542977452, 287.0332630706862, 283.43354511263334, 282.8431460953604, 280.9927509407349, 280.6873136475184], [280.3828506150961, 281.7898148785289, 282.3502574556245, 282.6614781892775, 287.44932665435255, 287.74333748594245, 287.3514894117984, 286.7575627660541, 282.9272610516072, 282.6150954507695, 281.3175373835582, 280.90393002836095], [280.554371661709, 281.94889351131815, 282.45773813442764, 282.65526179045474, 287.2850235871423, 287.5311817752957, 287.1287234306481, 286.48907380591675, 282.56855996279023, 282.3910231273234, 281.6944721056592, 281.2968907275414], [281.5620978677508, 282.24199515275177, 282.62128819071756, 282.67986785522334, 287.0842921080007, 287.5092683746633, 286.9507573596579, 286.25651696889395, 282.31760182230005, 282.10852130163386, 281.65875068855894, 281.26786405182446], [282.2239764776308, 281.88519598989086, 282.6533273462213, 282.37912440258094, 286.8614425262252, 287.55571046601744, 286.77581528655486, 286.0508732808481, 281.97036913576903, 282.45991459061344, 281.9185520340868, 281.5831343036522], [282.3940969534354, 282.0195900702006, 282.56715072962095, 282.58353406431314, 286.32493456593386, 287.76902059573916, 286.72039898665685, 285.8560790483717, 281.78480618045427, 282.7802638056041, 281.64914123680774, 281.8816494987988], [282.470590775961, 281.36320951954934, 282.839692506985, 281.61637068585685, 285.72521751749935, 288.1617858901928, 286.99692700737586, 284.88077520317006, 281.84195674306164, 283.00041316040966, 278.73487013379264, 280.77665002806685], [282.4276735850822, 0, 282.436064978821, 282.189783422795, 287.63571224540334, 286.9129105800757, 286.6796508106885, 285.5802136818004, 281.35108423398344, 281.76531630789657, 282.97343190263473, 0]]

file_dfmain = "/home/poyraden/Analysis/Homogenization_public/Files/madrid/DQA_nors80/Madrid_AllData_woudc.hdf"
#only needed for madrid (for the moment) to calculate means of the tmpump

##           end of the parts  TO BE CHANGED By HAND           ##
##                                                             ##

filefolder = '/DQA_nors80/'
file_ext = 'final_nors80_plusp'
##mm stands for monthly means

if main_rscorrection:
    filefolder = '/DQA_rs80/'
    file_ext = 'rs80'

path, allFiles, roc_table_file, dfmeta = station_inone(station_name)
humidity_correction, df_missing_tpump, calculate_current, organize_df, descent_data = station_inbool(station_name)
date_start_hom, ibg_split, sonde_tbc, rs80_begin, rs80_end = station_invar(station_name)


if df_missing_tpump:
    dfmain = pd.read_hdf(file_dfmain)
    dfmean = madrid_missing_tpump(dfmain)

if humidity_correction:
    dfmeta = calculate_cph(dfmeta)
    dfmeta.loc[:,'unc_cPH'] = dfmeta['cPH'].std()
    dfmeta.loc[:,'unc_cPL'] = dfmeta['cPL'].std()

clms = [i for i in range(1,13)]
table = pd.read_csv(roc_table_file,  skiprows=1, sep="\s *", names = clms,  header=None)


#read over all files to do the homogenization

for (filename) in (allFiles):
    file = open(filename, 'r')

    date_tmp = filename.split('/')[-1].split('.')[0][2:8]
    fullname = filename.split('/')[-1].split('.')[0]

    # date_tmp = filename.split('/')[-1].split("_")[1][2:8]
    # fullname = filename.split('/')[-1].split("_")[1]
    # # nmu.split('/')[-1].split("_")[1][2:8]

    date = datetime.strptime(date_tmp, '%y%m%d')
    datestr = date.strftime('%Y%m%d')


    # if datestr < date_start_hom: continue
    # print('one', datestr)

    # if datestr > '20050101': continue
    # if datestr < '20090101': continue

    # if datestr < '20190101': continue

    if datestr == '20170313': continue
    if datestr == '19920129': continue

    # if (int(datestr) < 20180101): continue
    # 920127
    # if int(datestr) > 20000103: continue
    #
    if int(datestr) < 20160601: continue


    # if datestr != '19930113': continue

    print(filename)

    df = pd.read_hdf(filename)
    dfm = dfmeta[dfmeta.Date == datestr]
    dfm = dfm.reset_index()
    if len(dfm) == 0:
        print('Check dfm')
        continue

    if len(dfm) == 1:
        dfm = dfmeta[dfmeta.Date == datestr][0:1]
    if (len(dfm) == 2) and search("2nd", fullname):
        dfm = dfmeta[dfmeta.Date == datestr][1:2]
    if(len(dfm) > 0) and not search("2nd", fullname):
        dfm = dfmeta[dfmeta.Date == datestr][0:1]
    dfm = dfm.reset_index()

    if organize_df:
        date_bool, df = df_station(df,datestr, dfm, station_name)
        if date_bool == 'stop':
            print('BAD File')
            continue
    if len(df) < 100: continue

    if df_missing_tpump:
        df = df_missing_variable(df, dfmean)

    if calculate_current:
        try:
            df = o3tocurrent(df, dfm)
        except (ValueError, KeyError):
            print('BAD File, check FILE')

    # input variables for hom.
    df['Tpump'] = df['TboxK']
    df['Tpump_original'] = df['TboxK']

    if scoresbysund_tpump:
        # middle = [-0.39753590663505634, -0.34941137614961804, -0.29216922413905877, -0.21226935342622255,
        #           -0.09855474724045621, -0.06481784648056532, -0.01940825095061882, -0.026262768870225273,
        #           0.0198915670325448, 0.02843701041339841, 0.2287331420904195, 0.371465237335201,
        #           0.5877013824654114, 0.6964017148621622, 0.9483028307058987, 1.1479365256078324,
        #           1.3599369865229107, 1.5091396506819592, 1.6441995812836296, 1.7164253403911687,
        #           1.7692913650572848, 1.8418493877254036, 1.9200557679865824, 1.9087723284806941,
        #           1.8473908436801594, 1.7223390743600646, 1.637501277369779, 1.379119722352499,
        #           1.227932457683238, 1.0207019945675597, 0.7442939080995927, 0.5144944460023737,
        #           0.10254409157653299, -0.29122231347088245, -0.6209911315433772, -0.5964160839160968]
        km_d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29, 30, 31, 32, 33, 34, 35, 36]
        km_u = [j + 1 for j in km_d]
        # print(km_u)


        df['Alt'] = df['Height'] / 1000
        # for k in range(len(km_d)):
        #     df.loc[(df.Alt > km_d[k]) & (df.Alt < km_u[k]), 'Tpump'] = df.loc[(df.Alt > km_d[k]) & (df.Alt < km_u[k]), 'Tpump'] + middle[k] + 10
        for k in range(len(km_d)-1):
            df['DateTime'] = pd.to_datetime(df['Date'], format='%Y%m%d')
            df['Datei'] = df['Date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d'))
            # print(type(df.DateTime.dtype))
            month = df.at[0, 'DateTime'].month
            # df.loc[(df.Date > '20160601') & (df.Alt > km_d[k]) & (df.Alt < km_u[k]), 'Tpump'] = mm[k][month - 1]
            #v2 for lower than mean values only
            # df.loc[(df.Date > '20160601') & (df.Alt > km_d[k]) & (df.Alt < km_u[k]) & (df.Tpump < mm[k][month - 1]),
            #        'Tpump'] = mm[k][month - 1]

            # print(month,k,  mm[k][month - 1])



    df['Phip'] = 100 / dfm.at[dfm.first_valid_index(), 'PF']
    df['Eta'] = 1

    df['dPhip'] = 0.02
    df['unc_cPH'] = dfm.at[dfm.first_valid_index(), 'unc_cPH']
    df['unc_cPL'] = dfm.at[dfm.first_valid_index(), 'unc_cPL']

    if not df_missing_tpump:
        df['unc_Tpump'] = 0.5  # case II-V
    #if there is missing tpump, the unc. is assgined in  function 'df_missing_variable'

    # #      radiosonde RS80 correction   #
    # # Electronic o3 sonde interface  was replaced with the transfer from RS80 to RS92  in 24 Nov 2005.
    rsmodel = ''
    bool_rscorrection = ''

    # if datestr < rs80_end and datestr >= rs80_begin:
    #     bool_rscorrection = True
    # # if datestr > rs80_end:
    # if datestr >= rs80_end or datestr < rs80_begin:
    #     bool_rscorrection = False
    # #
    #
    # if bool_rscorrection and main_rscorrection:
    #     df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
    #     df['Pair'] = df['Pair'] - df['Crs']

    # if main_rscorrection:
    #     df['Crs'], df['unc_Crs'] = RS_pressurecorrection(df, 'Height', rsmodel)
    #     df['Pair'] = df['Pair'] - df['Crs']

    df['Pair'] = df['Pair'] + 1.5

    #ROC calculation from the climatological means
    dfm = roc_values(dfm, df, table)


    # DQA corrections
    #      conversion efficiency        #
    df['alpha_o3'], df['unc_alpha_o3'] = absorption_efficiency(df, 'Pair', dfm.at[0,'SolutionVolume'])
    df['stoich'], df['unc_stoich'] = stoichmetry_conversion(df, 'Pair', dfm.at[0, 'SensorType'],
                                                            dfm.at[0, 'SolutionConcentration'], sonde_tbc)
    df['eta_c'], df['unc_eta_c'] = conversion_efficiency(df, 'alpha_o3', 'unc_alpha_o3', 'stoich', 'unc_stoich')

    #       background correction       #
    if station_name != 'scoresbysund':
        if dfm.at[0, 'string_bkg_used'] == 'ib2': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB2', ibg_split, station_name)
        if dfm.at[0, 'string_bkg_used']  == 'ib0': df['iBc'], df['unc_iBc'] = background_correction(df, dfmeta, dfm, 'iB0', ibg_split, station_name)
    if station_name == 'scoresbysund':
        df['iBc'], df['unc_iBc'] = background_correction_3split(df, dfmeta, dfm, 'iB2', '1993', '1995', '2017')

    if (df.Pair.min() <5) & (dfm.loc[0,'string_pump_location'] == 'case3'): print('HERE')
    #       pump temperature correction       #
    df['Tpump_cor'], df['unc_Tpump_cor'] = pumptemp_corr(df, dfm.loc[0,'string_pump_location'], 'Tpump', 'unc_Tpump', 'Pair')
    #      pump flow corrections        #
    # ground correction, humidity correction PTU
    if humidity_correction:
        df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab', True)
    if not humidity_correction:
        df['Phip_ground'], df['unc_Phip_ground'] = pf_groundcorrection(df, dfm, 'Phip', 'dPhip', 'TLab', 'PLab', 'ULab', False)
    # efficiency correction
    pumpflowtable = '999 '
    if dfm.at[0, 'SensorType'] == 'SPC': pumpflowtable = 'komhyr_86'
    if dfm.at[0, 'SensorType'] == 'DMT-Z': pumpflowtable = 'komhyr_95'
    # if test_ny: pumpflowtable = 'test_ny'

    # if test_ny:
    #     df['Cpf_t'], df['unc_Cpf_t'] = pumpflow_efficiency(df, 'Pair', 'test_ny', 'table_interpolate_nolog')
    #     df['Phip_eff_t'], df['unc_Phip_eff'] = return_phipcor(df, 'Phip', 'dPhip', 'Cpf_t', 'unc_Cpf')
    df['Cpf_t'], df['unc_Cpf_t'] = pumpflow_efficiency(df, 'Pair', 'test_ny', 'table_interpolate_nolog')
    df['Phip_eff_t'], df['unc_Phip_eff'] = return_phipcor(df, 'Phip', 'dPhip', 'Cpf_t', 'unc_Cpf')
    df['Cpf'], df['unc_Cpf'] = pumpflow_efficiency(df, 'Pair', pumpflowtable, 'table_interpolate')
    df['Phip_eff'], df['unc_Phip_eff'] = return_phipcor(df, 'Phip', 'dPhip', 'Cpf', 'unc_Cpf')
    df['Phip_cor'], df['unc_Phip_cor'] = return_phipcor(df, 'Phip_ground', 'unc_Phip_ground', 'Cpf', 'unc_Cpf')

    # all corrections
    df['O3_nc'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'Eta', 'Phip')
    df['O3c_eta'] = currenttopo3(df, 'I', 'Tpump', 'iB2', 'eta_c', 'Phip')
    df['O3c_etabkg'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip')
    df['O3c_etabkgtpump'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip')
    df['O3c_etabkgtpumpphigr'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_ground')
    df['O3c_etabkgtpumpphigref'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor')
    # df['O3c_ndacc1'] = currenttopo3(df, 'I', 'Tpump', 'ibg', 'Eta', 'Phip_eff')
    # if dfm.at[0, 'string_bkg_used'] == 'ib2':
    # df['O3c_ndacc'] = currenttopo3(df, 'I', 'Tpump', 'ibg', 'Eta', 'Phip_eff_t')
    # df['O3c_ndacc2'] = currenttopo3(df, 'I', 'Tpump', 'ibg', 'Eta', 'Phip_eff')
    #
    # df['O3c_ibg'] = currenttopo3(df, 'I', 'Tpump_cor', 'ibg', 'eta_c', 'Phip_cor')
    # df['O3c_tpump'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip_cor')
    # df['O3c_pf'] = currenttopo3(df, 'I', 'Tpump', 'iBc', 'eta_c', 'Phip_eff')
    df['O3c'] = currenttopo3(df, 'I', 'Tpump_cor', 'iBc', 'eta_c', 'Phip_cor')

    #to correct the data for negative O3c values, in case iBc is larger than I
    df.loc[(df.O3c < 0) & (df.O3c > -999) , 'O3c'] = 0

    # uncertainities
    df['dI'] = 0
    df.loc[df.I < 1, 'dI'] = 0.01
    df.loc[df.I >= 1, 'dI'] = 0.01 * df.loc[df.I > 1, 'I']
    df['dIall'] = (df['dI'] ** 2 + df['unc_iBc'] ** 2) / (df['I'] - df['iBc']) ** 2
    df['dEta'] = (df['unc_eta_c'] / df['eta_c']) ** 2
    df['dPhi_cor'] = (df['unc_Phip_cor'] / df['Phip_cor']) ** 2
    df['dTpump_cor'] = df['unc_Tpump_cor']
    # final uncertainity on O3
    df['dO3'] = np.sqrt(df['dIall'] + df['dEta'] + df['dPhi_cor'] + df['dTpump_cor'])

    # # check all the variables if they are in accepted value range

    if len(df[(df.O3c > -99) & (df.O3c < 0)]) > 0 | (len(df[df['O3c'] > 30]) > 0) :
        print('     BREAK       O3c')
    if (len(df[df['iBc'] > 0.5]) > 0) | (len(df[df.iBc.isnull()])>0):
        print('     BREAK       iBc')

    # TON calculations
    # if there is the descent data, remove those for TON calculation
    if descent_data:
        dfn = df[df.Height > 0]
        maxh = dfn.Height.max()

        index = dfn[dfn["Height"] == maxh].index[0]

        descent_list = dfn[dfn.index > index].index.tolist()
        dfa = dfn.drop(descent_list)

    if not descent_data:
        dfa = df.copy()

    dfa = dfa[(dfa.I > 0) & (dfa.I > -9) ]
    dfa = dfa[(dfa.O3c < 99) & (dfa.O3c > 0) ]

    dfm['O3Sonde_burst'] = o3_integrate(dfa, 'O3')
    dfm['O3Sonde_burst_raw'] = o3_integrate(dfa, 'O3_nc')
    dfm['O3Sonde_burst_hom'] = o3_integrate(dfa, 'O3c')

    if dfa['Pair'].min() < 10:
        dfa = dfa[dfa['Pair'] >= 10]

    if dfa['Pair'].min() < 33:

        # for woudc O3 values
        dfm['O3Sonde'] = o3_integrate(dfa, 'O3')
        dfm['O3SondeTotal'] = dfm['O3Sonde'] + dfm['ROC']
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = o3_integrate(dfa, 'O3c')
        dfm['O3SondeTotal_hom'] = dfm['O3Sonde_hom'] + dfm['ROC']
        # the same for raw no corrected o3 values
        dfm['O3Sonde_raw'] = o3_integrate(dfa, 'O3_nc')
        dfm['O3SondeTotal_raw'] = dfm['O3Sonde_raw'] + dfm['ROC']
        try:
            dfm['O3ratio'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal']
            dfm['O3ratio_hom'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_hom']
            dfm['O3ratio_raw'] = dfm['TotalO3_Col2A'] / dfm['O3SondeTotal_raw']
            if dfm.at[0, 'TotalO3_Col2A'] > 999:
                dfm['O3ratio'] = 9999
                dfm['O3ratio_hom'] = 9999
                dfm['O3ratio_raw'] = 9999
        except KeyError:
            dfm['O3ratio'] = 9999
            dfm['O3ratio_hom'] = 9999
            dfm['O3ratio_raw'] = 9999


    if df['Pair'].min() > 32:
        dfm['O3Sonde'] = 9999
        dfm['O3SondeTotal'] = 9999
        dfm['O3ratio'] = 9999
        dfm['O3Sonde_10hpa'] = 9999
        # the same for the homogenized O3 values
        dfm['O3Sonde_hom'] = 9999
        dfm['O3Sonde_10hpa_hom'] = 9999
        dfm['O3SondeTotal_hom'] = 9999
        dfm['O3ratio_hom'] = 9999
        dfm['O3Sonde_raw'] = 9999
        dfm['O3SondeTotal_raw'] = 9999
        dfm['O3ratio_raw'] = 9999

    #
    # print(dfm.at[0,'O3Sonde'], dfm.at[0,'O3Sonde_hom'], dfm.at[0,'ROC'],dfm.at[0,'O3Sonde'] + dfm.at[0,'ROC']  )
    # print(dfm.at[0,'O3SondeTotal'], dfm.at[0,'O3SondeTotal_hom'], df['Pair'].min())

    md_clist = ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
                'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'TLab', 'deltat', 'unc_deltat', 'unc_deltat_ppi', 'dEta']

    # merge all the metadata to md df and save it as a csv file
    for j in range(len(md_clist)):
        dfm.at[0, md_clist[j]] = df.at[df.first_valid_index(), md_clist[j]]

    dfm.to_csv(path + filefolder + datestr + "_o3smetadata_" + file_ext + ".csv")
    #
    # df = df.drop(
    #     ['Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'unc_eta',
    #      'unc_eta_c', 'dEta'], axis=1)

    # df = df.drop(
    #     ['Phip', 'Eta', 'unc_Tpump', 'unc_alpha_o3', 'alpha_o3', 'stoich', 'unc_stoich', 'eta_c', 'unc_eta',
    #      'unc_eta_c', 'iB2', 'iBc', 'unc_iBc', 'dEta'], axis=1)

    # data file that has data and uncertainties that depend on Pair or Height or Temperature
    df.to_hdf(path + filefolder + datestr + "_all_hom_" + file_ext + ".hdf", key='df')

    df['Tbox'] = df['Tpump_cor'] - k
    df['O3'] = df['O3c']

    # print(list(df))

    df = df_drop(df, station_name)

    # print(list(df))

    # df to be converted to WOUDC format together with the metadata
    df.to_hdf(path + filefolder + datestr + "_o3sdqa_" + file_ext + ".hdf", key='df')


########################################################################################################################

    # if len(df[(df.I > -99) & (df.I < 0)]) > 0 | (len(df[df['I'] > 30]) > 0) | (len(df[df.I.isnull()])>0):
    #     print('     BREAK       I')
    # if len(df[(df.Tpump_cor > -99) & (df.Tpump_cor < 0)]) > 0 | (len(df[df['Tpump_cor'] > 330]) > 0) :
    #     print('     BREAK       Tpump_cor', filename)
    # if (len(df[df.Tpump_cor.isnull()]) >0) & (df.Pair.min() >=5):
    #     print('BREAK Tpump 2 ')