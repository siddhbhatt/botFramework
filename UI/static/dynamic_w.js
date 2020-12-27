$(document).ready(function()

    {
	var x = 0; //Initial field counter
	var list_maxField = 10; //Input fields increment limitation
	
        //Once add button is clicked
	$('.list_add_button').click(function()
	    {
	    //Check maximum number of input fields
	    if(x < list_maxField){ 
	        x++; //Increment field counter
	        var list_fieldHTML = '<div style="border: thick solid black"><div class="row"><div class="col-xs-4 col-sm-4 col-md-4"><div class="form-group">Block Name<input name="list['+x+'][]" type="text" placeholder="Bolck Name" class="form-control"/></div></div><div class="col-xs-4 col-sm-4 col-md-4"><div class="form-group">Block Type<select name="blktype['+x+'][]" id="db" class="form-control"><option value="">..</option><option value="output">output</option><option value="input">input</option></select></div></div></div><div class="row"><div class="col-xs-7 col-sm-7 col-md-7"><div class="form-group">Get Variables<input autocomplete="on" name="getvariable['+x+'][]" type="text" placeholder="Get Variables Array" class="form-control"/></div></div></div><div class="row"><div class="col-xs-7 col-sm-7 col-md-7"><div class="form-group">Rules<input autocomplete="on" name="rules['+x+'][]" type="text" placeholder="Rules Array" class="form-control"/>   </div></div></div><div class="row"><div class="col-xs-11 col-sm-11 col-md-11">   <div class="form-group"><h4><b>Input Mapping</b></h4><div class="row"><div class="col-xs-4 col-sm-4 col-md-4">   <button class="btn btn-primary list_add_button_input" type="button">+ Add New Input</button></div></div><div class="row"><div class="col-xs-3 col-sm-3 col-md-3">   <div class="form-group">      Input Data      <input name="imdata['+x+'][]" type="text" placeholder="Input Data Function" class="form-control"/>   </div></div><div class="col-xs-3 col-sm-3 col-md-3">   <div class="form-group">      Input Channel      <input name="imchannel['+x+'][]" type="text" placeholder="Input Channel" class="form-control"/>   </div></div><div class="col-xs-3 col-sm-3 col-md-3">   <div class="form-group">      Input User      <input name="imuser['+x+'][]" type="text" placeholder="User Name" class="form-control"/>   </div></div></div>   </div></div></div><!--here for API--><div class="row"><div class="col-xs-11 col-sm-11 col-md-11">   <div class="form-group"><b><h4>API</h4></b><div class="row"><div class="col-xs-4 col-sm-4 col-md-4">   <button class="btn btn-primary list_add_button_api" type="button">+ Add New API Block</button></div></div><div class="row"><div class="col-xs-3 col-sm-3 col-md-3">   <div class="form-group">      End Point URL:      <input name="apiurl['+x+'][]" type="text" placeholder="https://hostname:portnumber" class="form-control"/>   </div></div><div class="col-xs-2 col-sm-2 col-md-2">   <div class="form-group">      Choose a API Type:      <select name="apitype['+x+'][]" id="db" class="form-control">         <option value="">..</option>         <option value="GET">GET</option>         <option value="POST">POST</option>         <option value="POST">PUT</option>      </select>   </div></div><div class="col-xs-3 col-sm-3 col-md-3">   <div class="form-group">      API Params Array:      <input name="apiparams['+x+'][]" type="text" placeholder="[{key: null, value: null}]" class="form-control"/>   </div></div><div class="col-xs-4 col-sm-4 col-md-4">   <div class="form-group">      Output Tag      <input name="apiouttag['+x+'][]" type="text" placeholder="[{map:{name:null,path:[],outputFormat:null,outputTag:null}}]" class="form-control"/>   </div></div></div>   </div></div></div><div class="col-xs-7 col-sm-7 col-md-7"><a href="javascript:void(0);" class="list_remove_button btn btn-danger">Remove Block</a></div></div></div>'; //New input field html 
	        $('.list_wrapper').append(list_fieldHTML); //Add field html
	    }
        });
    
        //Once remove button is clicked
        $('.list_wrapper').on('click', '.list_remove_button', function()
        {
           $(this).closest('div.row').remove(); //Remove field html
           x--; //Decrement field counter
        });
});