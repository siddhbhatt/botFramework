class pageBuild:
    HTMLTextHead="""<html><head></head><body><div><form>"""
    HTMLTextTail="""<input type="submit" name="action" value="Upload"></input></form></div></body></html>"""
    #HTMLTagFieldName="""Intents Patterns:"""
    def __init__(self):
        pass
    def textarea(text,HTMLTagFieldName):
        txtbuild=HTMLTagFieldName+'<textarea>'+text+'</textarea></br>'
        return txtbuild
    def field(text,HTMLTagFieldName,idval):
        textbuild='<label for="'+HTMLTagFieldName+'">'+HTMLTagFieldName+': </label><input type="text" id="textval'+str(idval)+'" name="textval'+str(idval)+'" value="'+text+'"><br><br>'
        return textbuild
    def selectarea(self):
        pass
    def dropdown(engtext,xlevel,selectedval,*options):
        dropdownhead='<label for="'+xlevel+'">Choose a '+engtext+':</label><select id="'+xlevel+'">'
        dropdownfooter='</select>'
        cc=''
        for xoptios in list(options):
            cc=cc+'<option value="'+xoptios+'">'+xoptios+'</option>'
        fulltext=dropdownhead+'<option value="'+selectedval+'" selected>'+selectedval+'</option>'+cc+dropdownfooter
        return fulltext
    def checkbox(self):
        pass