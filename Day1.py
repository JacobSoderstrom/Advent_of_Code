#Creating a input string
d="42812249899758728399611695139795793356913694984837941712536253226986946118574311373399233137985644636248212964655628661154375656427571535987492489811342447278297478946434862627853293622888178627358627888657582823936679442922331747672233742439923998615367527592411332256187381436445133918691881345168526319289162718676981812871559571544456544458151467752187493594291354712175185163137331612249147156469773129895198951191727268433546343621828326196215867126662529918876458981451879357637562916389634966531299128577659514214626179224447572178294136478796892453784169853828845935515978398563818725465385186487454458487899919324264161185975672863462385347563847892374447156384563546817382419668436193426945945912426919681151292744266276156382432362175878586639142477868359917944784559593192858925593595329511193743126681535278139996729538933962617866414841556117538672599246978288875794255836211793862936912943971742747441685162812119163935564639427645184713118265248656141594281581878588455919348387"
d=d+"813935184163336639878865784439692542321766251735648619382134145488928326669122477872383339791422439672255959395912531717589959468552485241949579338948183135478728745236714566182928751877163193931468313772249353131818131521634299414168348411196947695294637831488342167795239758861356295874132898773456549237897739643148121598365681448651886564264561241394512948546497953599167577633878675899712812465131115318281618892493518636181379725199764399268629472469928196947314272111643296821643497768413818448196384514148679399647679395422622588543242265439443988284216329545854975513724761433289918799666659254665451118997149437165711133264794329259392279967999512794857228367544577376681918459145667322859284537818187922364478161274924459939458944356927998392174672539862182131312497868333339363322577951919379426886681826294891916931541841773981864624813168346787337136148894393529761447261622146489221597199791437358154786339126331853345294847793228186114381945222922787876537633289444215165691811"
d=d+"78517915745625295158611636365253948455727653672922299582352766484"
#Converting the inpus string to list of numbers and initiating sum to zero
d=[int(num) for num in d]
sum=0

#for each position in list check if current value is same as previous. Convert bolean to 0/1 and multiply with current value and add to sum
for i in range(len(d)):
    sum=sum+d[i]*int(d[i-1]==d[i])
#print total sum
print(sum)
