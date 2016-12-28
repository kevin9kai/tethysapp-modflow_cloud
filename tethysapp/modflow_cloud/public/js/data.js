$(document).ready(function(){

})

function download_hs_res(res_id)
{

window.location = '/apps/modflow-cloud/download-hs-res/?my_res_id=' + res_id;
//BY adding a / before url it is a relative. If only in '' then absolute

//window.location is browser's location. So where it is.


}


