window.onload = function(){
  document.addEventListener('DOMContentLoaded', function() {
      document.getElementById('myBtn').addEventListener('click', () => {
      document.querySelector('.bg-modal').style.display ='flex';
      $('#btnToken').val("1");
      });
      document.getElementById('myBtn2').addEventListener('click', () => {
      document.querySelector('.bg-modal').style.display ='flex';
      $('#btnToken').val("2");
      });
      document.querySelector(".close").addEventListener('click',() => {
      document.querySelector('.bg-modal').style.display ='none';
      });
  });
};
window.onload = function(){
  document.addEventListener('DOMContentLoaded', function() {
      document.getElementById('btn-search').addEventListener('click', () => {
      $('#town').children('option:not(:first)').remove();
      $('#whatinput').children('label').remove();
      document.querySelector('.bg-modal2').style.display ='flex';
      });
      document.querySelector(".close2").addEventListener('click',() => {
      document.querySelector('.bg-modal2').style.display ='none';
      });
  });
};
$(".btn-search").click(function(){
  var town_input = document.getElementById('town_input').value;
  $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: 'townsearch/', // 통신할 url을 지정
    data: {'town_input': town_input, 'csrfmiddlewaretoken': '{{ csrf_token }}'}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    success: function(data){ 
      for (var i in data['town_input']) {    
        var div = document.createElement('option');
        div.innerHTML = data['town_input'][i];
        document.getElementById('town').appendChild(div);
      }
      var div = document.createElement('label');
      div.innerHTML = '"'+town_input+'"으로 검색 결과';
      document.getElementById('whatinput').appendChild(div);
    },
    error: function(request, status, error){ // 통신 실패시 - 리다이렉트
      alert("wrong input")
      window.location.replace("/")
    },
  });
})

$(".btn-2").click(function(){
  var town_input=$("#town option:selected").val()
  var btnToken=$("#btnToken").val()
  alert(btnToken)
  $.ajax({ // .like 버튼을 클릭하면 <새로고침> 없이 ajax로 서버와 통신하겠다.
    type: "POST", // 데이터를 전송하는 방법을 지정
    url: 'townenroll/', // 통신할 url을 지정
    data: {'town_input': town_input, 'btnToken': btnToken,'csrfmiddlewaretoken': '{{ csrf_token }}'}, // 서버로 데이터 전송시 옵션
    dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정, 없으면 알아서 판단
    // 서버측에서 전송한 Response 데이터 형식 (json)
    success: function(data){ 
      document.querySelector('.bg-modal2').style.display ='none';
      document.querySelector('.bg-modal').style.display ='none';
      window.location.replace("/mypage")
    },
    error: function(request, status, error){ // 통신 실패시 - 리다이렉트
      alert("wrong input")
      window.location.replace("/")
    },
  });
})
