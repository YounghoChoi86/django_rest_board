function addBoardHeader(item) {
    var boardHeader = "<tr>";
    for (key in item) {
      if (key == 'url') {
        continue;
      }
      boardHeader += "<th>" + key + "</th>";
    }
    boardHeader += "</tr>"
    return boardHeader;
}

function makePostingDetailTable(posting, id) {
  var tableTag = "<table class='table table-hover'>"
  if (posting) {
    for (key in posting) {
      tableTag += '<tr><td>' + key + '</td><td>' + posting[key] + '</td></tr>';
    }
  }
  tableTag += '</table>'
  $('#' + id).append(tableTag);
  console.log($('#' + id));
}
function postingDetailClear() {
  $('#posting-detail').empty()
}

function postingDetailView(url, clearOption) {
  console.log(url);
  $.ajax({
    type: "GET",
    url:  url,
    async: true,
    success : function(data) {
      var posting = data;
      console.log(posting);
      console.log(posting.length);
      if (posting) {
        if (clearOption) {
          //$('#board-list').empty();
          $('#posting-detail').empty();
        }
        makePostingDetailTable(posting, 'posting-detail')
        $('#posting-detail').append('<button class="btn btn-primary" onclick="javascript:postingDetailClear()">닫기</button>');
      }
    }
  })
}

function addBoadItem(item) {
  var boardItem = "<tr>";

  for (key in item) {
    if (key == 'url') {
      continue;
    }
    else if (key == 'title') {
      boardItem += "<td> <a href='javascript:postingDetailView(\"" + item['url'] + "\", true)';>" + item[key] + "</a></td>";
      console.log(boardItem)
    }
    else {
      boardItem += "<td>" + item[key] + "</td>";
    }
  }
  boardItem += "</tr>";
  return boardItem;
}

function getPostings(pageNum, clearOption){
  $.ajax({
    type: "GET",
    url:  "/api/postings?page=" + pageNum,
    async: true,
    success : function(data) {
      var postings = data['results'];
      console.log(postings)
      if (postings.length > 0) {
        if (clearOption) {
          $('#board-list').empty();
        }
        $('#board-list').append(addBoardHeader(postings[0]));
        for (var i = 0, item; item=postings[i]; i++) {
          console.log(postings[i]);
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

function makePageNation(index) {
  $.ajax({
    type: "GET",
    url: "/api/postings/count",
    async: true,
    success: function(data) {
      var count = data['count'];
      var pageSize = data['postingPerPage'];

      pageNum = getPageNum(count, pageSize)
      if (index > 0) {
        $('#page').append('<a href="#" class="page-link" aria-label="Previous"> <span aria-hidden="true">&laquo;</span></a>');
      }
      for (var i = index; i < pageNum; i++) {
        $('#page').append('<li class="page-item"><a class="page-link" href="javascript:getPostings('+ (i + 1) + "," + true +');">' + (i + 1) + '</a></li>');
      }
      if (pageNum > 5) {
        $('#page').append('<a href="#" class="page-link" aria-label="Next"> <span aria-hidden="true">&raquo;</span></a>');
      }
    }
  })
}
