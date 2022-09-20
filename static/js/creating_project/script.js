// const data="";
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function openDropdown_1() {
    document.getElementById("myDropdown_1").classList.toggle("show");
}

function closeDropdown_1() {
    var dropdowns = document.getElementsByClassName("dropdown-content_1");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
            }
        }
    }


function openDropdown_2() {
    document.getElementById("myDropdown_2").classList.toggle("show");
}

function closeDropdown_2() {
    var dropdowns = document.getElementsByClassName("dropdown-content_2");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
            }
        }
    }


function openDropdown_3() {
    document.getElementById("myDropdown_3").classList.toggle("show");
}

function closeDropdown_3() {
    var dropdowns = document.getElementsByClassName("dropdown-content_3");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
            }
        }
    }



function openDropdown_4() {
    document.getElementById("myDropdown_4").classList.toggle("show");
}

function closeDropdown_4() {
    var dropdowns = document.getElementsByClassName("dropdown-content_4");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
            }
        }
    }


function openDropdown_5() {
    document.getElementById("myDropdown_5").classList.toggle("show");
}

function closeDropdown_5() {
    var dropdowns = document.getElementsByClassName("dropdown-content_5");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
            }
        }
}

function SendData(url, csrf, field_name, field_data){
    const fd = new FormData();
    fd.append('csrfmiddlewaretoken', csrf)
    fd.append(`${field_name}`, `${field_data}`)
    $.ajax( {
        type : 'POST' ,
        url : url ,
        enctype : ' multipart/form-data' ,
        data : fd,
        cache:false,
        contentType: false,
        processData: false,
    })
}


function UpdateData(){
    url = '';
    request = $.ajax( {
        type : 'GET' ,
        url : url ,
    })
    alert(request.data);
}


function OpenProjectName(){
    document.getElementById("project_name_button").classList.remove("show");
    document.getElementById("project_name_button").classList.toggle("hide");
    document.getElementById("project_name_input").classList.toggle("show");
    document.getElementById("project_name_input").classList.remove("hide");
}

function CloseProjectName(){
    document.getElementById("project_name_button").classList.toggle("show");
    document.getElementById("project_name_button").classList.remove("hide");
    document.getElementById("project_name_input").classList.remove("show");
    document.getElementById("project_name_input").classList.toggle("hide");
}


function OpenProjectType(){
    document.getElementById("project_type_button").classList.remove("show");
    document.getElementById("project_type_button").classList.toggle("hide");
    document.getElementById("project_type_input").classList.toggle("show");
    document.getElementById("project_type_input").classList.remove("hide");
}

function CloseProjectType(){
    document.getElementById("project_type_button").classList.toggle("show");
    document.getElementById("project_type_button").classList.remove("hide");
    document.getElementById("project_type_input").classList.remove("show");
    document.getElementById("project_type_input").classList.toggle("hide");
}


function OpenProjectDescription(){
    document.getElementById("project_description_button").classList.remove("show");
    document.getElementById("project_description_button").classList.toggle("hide");
    document.getElementById("project_description_input").classList.toggle("show");
    document.getElementById("project_description_input").classList.remove("hide");
}

function CloseProjectDescription(){
    document.getElementById("project_description_button").classList.toggle("show");
    document.getElementById("project_description_button").classList.remove("hide");
    document.getElementById("project_description_input").classList.remove("show");
    document.getElementById("project_description_input").classList.toggle("hide");
}


function OpenProjectEmployeeInterests(){
    document.getElementById("project_employee_interests_button").classList.remove("show");
    document.getElementById("project_employee_interests_button").classList.toggle("hide");
    document.getElementById("project_employee_interests_input").classList.toggle("show");
    document.getElementById("project_employee_interests_input").classList.remove("hide");
}

function CloseProjectEmployeeInterests(){
    document.getElementById("project_employee_interests_button").classList.toggle("show");
    document.getElementById("project_employee_interests_button").classList.remove("hide");
    document.getElementById("project_employee_interests_input").classList.remove("show");
    document.getElementById("project_employee_interests_input").classList.toggle("hide");
}


function OpenProjectPriceNoMore(){
    document.getElementById("project_price_no_more_button").classList.remove("show");
    document.getElementById("project_price_no_more_button").classList.toggle("hide");
    document.getElementById("project_price_no_more_input").classList.toggle("show");
    document.getElementById("project_price_no_more_input").classList.remove("hide");
}

function CloseProjectPriceNoMore(){
    document.getElementById("project_price_no_more_button").classList.toggle("show");
    document.getElementById("project_price_no_more_button").classList.remove("hide");
    document.getElementById("project_price_no_more_input").classList.remove("show");
    document.getElementById("project_price_no_more_input").classList.toggle("hide");
}

function GetData(url){
    $.ajax({
        url: url, 
        success: function data(data){
            $("#project_name_a_value").html(data['name']);
            $("#project_name_input_value").val(data['name']);

            $("#project_type_a_value").html(data['type']);
            
            $("#project_description_a_value").html(data['description'].substring(0, 25)+"...");
            $("#project_description_input_value").val(data['description']);

            $("#project_price_no_more_a_value").html(data['price_no_more'] + data['currency']);
            $("#project_price_no_more").val(data['price_no_more']);
            $("#CURRENCY").val(data['currency']);
        }
      })

    
}


function CheckAndSendName(){
    let csrf = document.getElementsByName('csrfmiddlewaretoken');
    let data = document.getElementsByName('project_name');
    if ((data[0].value.length >= 5) && (data[0].value.length <= 30)){
        SendData('', csrf[0].value, 'project_name', data[0].value);
        CloseProjectName();
        $("#project_name_error_value").html("");
        GetData('get_data');
    }else{
        $("#project_name_error_value").html("От 5 до 30 символов");
    }
}   


function CheckAndSendType(type){
    let csrf = document.getElementsByName('csrfmiddlewaretoken');
    SendData('', csrf[0].value, `project_type_${type}`, '');
    CloseProjectType();
    GetData('get_data');
}


function CheckAndSendDescription(){
    let csrf = document.getElementsByName('csrfmiddlewaretoken');
    let data = document.getElementsByName('project_description');
    if ((data[0].value.length >= 5) && (data[0].value.length <= 300)){
        SendData('', csrf[0].value, 'project_description', data[0].value);
        CloseProjectDescription();
        $("#project_description_error_value").html("");
        GetData('get_data');
    }else{
        $("#project_description_error_value").html("От 5 до 300 символов");
    }
}


function CheckAndSendEmployeeInterests(){
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let data_1 = document.getElementsByName('project_employee_interest_1');
    let data_2 = document.getElementsByName('project_employee_interest_2');
    let data_3 = document.getElementsByName('project_employee_interest_3');
    let coincidences = false;

    if ((data_1[0].value != "") && (data_2[0].value != "")){
        if (data_1[0].value == data_2[0].value){
            coincidences = true;
        }
    }
    if ((data_2[0].value != "") && (data_3[0].value != "")){
        if (data_2[0].value == data_3[0].value){
            coincidences = true;
        }
    }
    if ((data_1[0].value != "") && (data_3[0].value != "")){
        if (data_1[0].value == data_3[0].value){
            coincidences = true;
        }
    }

    if ((data_1[0].value != "") || (data_2[0].value != "") || (data_3[0].value != "")){
        if (coincidences == false){
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf)
            fd.append(`project_employee_interest_1`, `${data_1[0].value}`)
            fd.append(`project_employee_interest_2`, `${data_2[0].value}`)
            fd.append(`project_employee_interest_3`, `${data_3[0].value}`)
            $.ajax( {
                type : 'POST' ,
                url : "" ,
                enctype : ' multipart/form-data' ,
                data : fd,
                cache:false,
                contentType: false,
                processData: false,
            })
            CloseProjectEmployeeInterests();
            $("#project_employee_interests_error_value").html("");
            GetData('get_data');
        }else{
            $("#project_employee_interests_error_value").html("От 5 до 300 символов");
        }
    }else{
        CloseProjectEmployeeInterests();
    }
}


function CheckAndSendPriceNoMore(){
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let price_no_more = document.getElementsByName('project_price_no_more');
    let currency = document.getElementsByName('currency');
    

        if (!isNaN(`${price_no_more[0].value.replace(/\s/g, '')}`)){
            const fd = new FormData();
            fd.append('csrfmiddlewaretoken', csrf)
            fd.append(`project_price_no_more`, `${price_no_more[0].value}`)
            fd.append(`currency`, `${currency[0].value}`)
            $.ajax( {
                type : 'POST' ,
                url : "" ,
                enctype : ' multipart/form-data' ,
                data : fd,
                cache:false,
                contentType: false,
                processData: false,
            })
            CloseProjectPriceNoMore();
            $("#project_price_no_more_error_value").html("");
            GetData('get_data');
        }else{
            $("#project_price_no_more_error_value").html("В поле для числа не может быть других символов");
        }

    
}


function AcceptCreatingProject() {
    $.ajax({
        url: "", 
        success: function data(data){
            if ((data['name'] != "") && (data['type'] != "") && (data['description'] != "") && (data['category'] != "") && (data['subcategory'] != "") && (data['employee_interests'] != "") && (data['price_no_more'] != "") && (data['currency'] != "")){
                $.ajax({
                    url: "final_check_list_view", 
                    success: function data(data){
                        let json = JSON.parse(data);
                        alert(data.length);
                        if (data.length == 2){
                            csrf = document.getElementsByName('csrfmiddlewaretoken');
                            let form = document.getElementById('ACCEPT');
                            form.submit();
                        }else{
                            if ('name' in json){
                                $("#project_submit_error_value").html(json["name"]);
                            }else if ('description' in json){
                                $("#project_submit_error_value").html(json["description"]);
                            }else if ('type' in json){
                                $("#project_submit_error_value").html(json["type"]);
                            }else if ('category' in json){
                                $("#project_submit_error_value").html(json["category"]);
                            }else if ('subcategory' in json){
                                $("#project_submit_error_value").html(json["subcategory"]);
                            }else if ('subsubcategory' in json){
                                $("#project_submit_error_value").html(json["subsubcategory"]);
                            }else if ('employee_interests' in json){
                                $("#project_submit_error_value").html(json["employee_interests"]);
                            }else if ('price_no_more' in json){
                                $("#project_submit_error_value").html(json["price_no_more"]);
                            }else{
                                $("#project_submit_error_value").html("Ошибка!!!");
                            }
                            
                            
                        }
                    }
                  })
                
            }else{
                $("#project_submit_error_value").html("Заполните все поля");
            }
            
        }
      })
}