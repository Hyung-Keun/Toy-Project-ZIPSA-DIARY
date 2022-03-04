const count = parseInt($("#diary_count").val());
const total_count = parseInt($("#total_count").val());
let skipIndex = parseInt(count);
const limit = parseInt(count);

function infinity(){
  window.onscroll = function(e){
    if((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
      if(total_count <= skipIndex) {
        return false;
      } else {
        $.ajax({
          type: "GET",
          url: "/api/diary",
          data: {
              skipIndex: skipIndex,
              limit: limit
          },
          success: function (response) {
              const diary = (response['diary'])
              const file_url = "/static/img/";
              $.each(diary, function (index, diary) {
                  let appendInfo = `<div class="card" style="width: 350px">
                                    <img src="${file_url + diary.diary_file}" class="card-img-top" alt="...">
                                    <div class="card-header">
                                      <h5 class="text-center">
                                        <a href="diary/${diary._id}">${diary.diary_title}</a>
                                      </h5>
                                      </div>
                                      <ul class="list-group list-group-flush">
                                        <li class="list-group-item">${diary.review_content}</li>
                                        <li class="list-group-item">${diary.diary_create_date}</li>
                                        <li class="list-group-item">${diary.author}</li>
                                    </ul>
                                </div>`
                $("#diary_list").append(appendInfo);
                skipIndex++;
            })

          }
        })
      }
    }
  }
}
infinity();

