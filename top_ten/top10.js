$(document).ready(function (){
//alert ('doc ready');

    $('#button').on('click', function()
    {
        var from = document.getElementById("myDate").value;
        var to = document.getElementById("myDate1").value;
        var hour = $('#select-box-hour').val();
        var hour2 = $('#select-box-hour1').val();
        var selected_val = $("#select-box option:selected").attr('value');

        var fromDateParts = from.split('-'),
            toDateParts = to.split('-'),
            newFromDate=fromDateParts[0]+"/"+fromDateParts[1]+"/"+fromDateParts[2],
            newToDate=toDateParts[0]+"/"+toDateParts[1]+"/"+toDateParts[2];
        var timestampFrom = (new Date(newFromDate).getTime()) + (hour*3600000),
            timestampTo = (new Date(newToDate).getTime()) + (hour*3600000);
      

      var request = $.ajax({'url': '/getTopTen?timeFrom='+timestampFrom+'&timeTo='+timestampTo + '&direction=' + selected_val});
      //console.log(request);
      request.done(function(response)
      {  
        //console.log(response.result[0]["avg_speed"]);
        var selected_val = $("#select-box option:selected").attr('value');
        if(selected_val==2){
            $('#speed1').text(response.result[0]["avg_speed"]);
            $('#location1').text(response.result[0]["location"]);
            $('#speed2').text(response.result[1]["avg_speed"]);
            $('#location2').text(response.result[1]["location"]);
            $('#speed3').text(response.result[2]["avg_speed"]);
            $('#location3').text(response.result[2]["location"]);
            $('#speed4').text(response.result[3]["avg_speed"]);
            $('#location4').text(response.result[3]["location"]);
            $('#speed5').text(response.result[4]["avg_speed"]);
            $('#location5').text(response.result[4]["location"]);
            $('#speed6').text(response.result[5]["avg_speed"]);
            $('#location6').text(response.result[5]["location"]);
            $('#speed7').text(response.result[6]["avg_speed"]);
            $('#location7').text(response.result[6]["location"]);
            $('#speed8').text(response.result[7]["avg_speed"]);
            $('#location8').text(response.result[7]["location"]);
            $('#speed9').text(response.result[8]["avg_speed"]);
            $('#location9').text(response.result[8]["location"]);
            $('#speed10').text(response.result[9]["avg_speed"]);
            $('#location10').text(response.result[9]["location"]);
        }
        else if(selected_val==3) {
            $('#speed1').text(response.result_ne[0]["avg_speed"]);
            $('#speed2').text(response.result_ne[1]["avg_speed"]);
            $('#speed3').text(response.result_ne[2]["avg_speed"]);
            $('#speed4').text(response.result_ne[3]["avg_speed"]);
            $('#speed5').text(response.result_ne[4]["avg_speed"]);
            $('#speed6').text(response.result_ne[5]["avg_speed"]);
            $('#speed7').text(response.result_ne[6]["avg_speed"]);
            $('#speed8').text(response.result_ne[7]["avg_speed"]);
            $('#speed9').text(response.result_ne[8]["avg_speed"]);
            $('#speed10').text(response.result_ne[9]["avg_speed"]);

            $('#location1').text(response.result_ne[0]["location"]);
            $('#location2').text(response.result_ne[1]["location"]);
            $('#location3').text(response.result_ne[2]["location"]);
            $('#location4').text(response.result_ne[3]["location"]);
            $('#location5').text(response.result_ne[4]["location"]);
            $('#location6').text(response.result_ne[5]["location"]);
            $('#location7').text(response.result_ne[6]["location"]);
            $('#location8').text(response.result_ne[7]["location"]);
            $('#location9').text(response.result_ne[8]["location"]);
            $('#location10').text(response.result_ne[9]["location"]);
        }
        else{
        }
      });
      request.fail(function(jqXHR, textStatus)
      {
        alert('Request failed: ' + textStatus);
      });
    });


    $('#button1').on('click', function()
    {


        //alert(timestampFrom);
        //var request = $.ajax({'url': '/getTopTen'});
        request.done(function(response)
        {

        });
        request.fail(function(jqXHR, textStatus)
        {
            alert('Request failed: ' + textStatus);
        });
    });
/*
//hide all tabs first

    $('.tab-content').hide();

//show the first tab content
    $('#tab-1').show();

    $('#select-box').change(function () {
        //alert("slect change detected");
        port_num = $('#select-box').val();
        //first hide all tabs again when a new option is selected
        $('.tab-content').hide();
        //then show the tab content of whatever option value was selected
        $('#' + "tab-" + port_num).show();
        //
    });
*/

});
