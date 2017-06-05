var restKeyToKoreanMap = {
  "name" : "작성자",
  "title" : "제목",
  "text" : "내용",
  "create_date" : "작성일",
  "id" : "#",
};
function addBoardHeader(item) {
    var boardHeader = "<tr>";
    for (key in item) {
      if (key == 'url' || key == 'comment_count') {
        //console.log(key)
        continue;
      }
      boardHeader += "<th>" + restKeyToKoreanMap[key] + "</th>";
    }
    boardHeader += "</tr>"
    return boardHeader;
}

function addBoadItem(item) {
  var boardItem = "<tr>";

  for (key in item) {
    if (key == 'url' || key == 'comment_count') {
      //console.log(key)
      continue;
    }
    else if (key == 'title') {
      boardItem += "<td> <a href='javascript:postingDetailView(\"" + item['url'] + "\", true)';>" + item[key] + "["+ item['comment_count'] +"]"+ "</a></td>";
      //console.log(boardItem)
    }
    else {
      boardItem += "<td>" + item[key] + "</td>";
    }
  }
  boardItem += "</tr>";
  return boardItem;
}

function makePostingDetailTable(posting, id) {
  var tableTag = "<table class='table table-hover'>"
  if (posting) {
    for (key in posting) {
      tableTag += '<tr><td>' + restKeyToKoreanMap[key] + '</td><td>' + posting[key] + '</td></tr>';
    }
  }
  tableTag += '</table>'
  $('#' + id).append(tableTag);
  //console.log($('#' + id));
}
function postingDetailClear() {
  $('#posting-detail').empty()
}

function postingDelete(id) {
  console.log(id);
  console.log('postingDelete');
  $.ajax({
    type: "DELETE",
    url: "/api/postings/" + id,
    async: true,
    success: function(data) {
      alert('지우는데 성공하였습니다.');
      postingDetailClear();
      getPostings(1, true);
      makePageNation(0);
    },
    error: function(data) {
      alert('지우는데 실패하였습니다.');
    }
  });
}

function postingDetailView(url, clearOption) {
  $.ajax({
    type: "GET",
    url:  url,
    async: true,
    success : function(data) {
      var posting = data;

      if (posting) {
        if (clearOption) {
          $('#posting-detail').empty();
        }
        makePostingDetailTable(posting, 'posting-detail');

        $('#posting-detail').append('<button class="btn btn-primary">수정</button>');
        console.log('<button class="btn btn-primary" onclick="javascript:postingDelete(' + data['id'] + ');">삭제</button>');
        $('#posting-detail').append('<button class="btn btn-primary" onclick="javascript:postingDelete(' + data['id'] + ');">삭제</button>');
        $('#posting-detail').append('<button class="btn btn-primary" onclick="javascript:postingDetailClear();">닫기</button>');
      }
    }
  })
}



function getPostings(pageNum, clearOption){
  $.ajax({
    type: "GET",
    url:  "/api/postings?page=" + pageNum,
    async: true,
    success : function(data) {
      var postings = data['results'];
      //console.log(postings)
      if (postings.length > 0) {
        if (clearOption) {
          $('#board-list').empty();
        }
        $('#board-list').append(addBoardHeader(postings[0]));
        for (var i = 0, item; item=postings[i]; i++) {
          //console.log(postings[i]);
          $('#board-list').append(addBoadItem(postings[i]));
        }
      }
    }
  })
}

function getPageNum(count, pageSize) {
    if (count == 0) {
      return 0;
    }
    else if (count % pageSize == 0) {
      return (count / pageSize);
    }
    return parseInt((count / pageSize) + 1);
}



function makePageNation(startIndex) {
  $.ajax({
    type: "GET",
    url: "/api/postings/count",
    async: true,
    success: function(data) {
      var count = data['count'];
      var pageSize = data['postingPerPage'];

      pageNum = getPageNum(count, pageSize);
      $('#page').empty();
      //console.log(pageNum)
      if (startIndex > 0) {
        $('#page').append('<a href="#" class="page-link" aria-label="Previous"> <span aria-hidden="true">&laquo;</span></a>');
      }
      for (var i = startIndex; i < pageNum; i++) {
        $('#page').append('<li class="page-item"><a class="page-link" href="javascript:getPostings('+ (i + 1) + "," + true +');">' + (i + 1) + '</a></li>');
      }
      if (pageNum > 5) {
        $('#page').append('<a href="#" class="page-link" aria-label="Next"> <span aria-hidden="true">&raquo;</span></a>');
      }
    }
  })
}

function closeWriteForm() {
  console.log("closeWriteForm")
  $('#write-form').empty()
}

function submitWriteForm() {

  var posting = {
     name: $("#form-name").val(),
     title:$("#form-title").val(),
     text :$("#form-text").val()
  }
  $('#write-form').html('sending..');
  $.ajax({
    url: '/api/postings/',
    type: 'post',
    async: true,
    data: JSON.stringify(posting),
    contentType: "application/json; charset=utf-8",
    dataType: 'json',
    success: function (data) {
      $('#write-form').html('<div class="alert alert-success alert-dismissible fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>게시물을 등록하였습니다.</strong></div>');
    },
    error: function(data) {
      $('#write-form').html('<div class="alert alert-success alert-dismissible fade show" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>게시물을 등록에 실패하였습니다.</strong></div>');
    }
  });

  return false;
}



function makeWriteForm() {
  $('#write-form').empty();
  $('#write-form').append('<div class="form-group"><label for="제목">제목</label><input type="text" class="form-control" id="form-title" rows="3"></div>');
  $('#write-form').append('<div class="form-group"><label for="작성자">작성자</label><input type="text" class="form-control" id="form-name" rows="3"></div>');
  $('#write-form').append('<div class="form-group"><label for="내용">내용</label><textarea class="form-control" id="form-text" rows="3"></textarea></div>');
  $('#write-form').append('<button class="btn btn-primary" onclick="javascript:return submitWriteForm();">완료</button>');
  $('#write-form').append('<button class="btn btn-primary" onclick="javascript:closeWriteForm();">닫기</button>');
}
