// save toggled elements in a list to toggle their 'hidden' back after modal closes
var toggledElts = []
var selectedCourse = null

const overlay = document.querySelector('.modal-overlay')
overlay.addEventListener('click', toggleModal)

document.querySelectorAll('.modal-close').forEach((modal)=>{
    modal.addEventListener('click', toggleModal)
})

document.onkeydown = function(evt) {
  evt = evt || window.event
  var isEscape = false
  if ("key" in evt) {
    isEscape = (evt.key === "Escape" || evt.key === "Esc")
  } else {
    isEscape = (evt.keyCode === 27)
  }
  if (isEscape && document.body.classList.contains('modal-active')) {
    toggleModal()
  }
};

function toggleModal(course) {
    selectedCourse = course
    const body = document.querySelector('body')
    const modal = document.querySelector('.modal')
    modal.classList.toggle('opacity-0')
    modal.classList.toggle('pointer-events-none')
    var isToggled = body.classList.toggle('modal-active')

    if (isToggled) {

        // untoggle previous text
        toggledElts.forEach((elt) => {
            elt.classList.toggle('hidden')
        })
        toggledElts = []

        const data = JSON.parse(course)
        var title = document.getElementById('modalTitle').innerText = 'Add ' + data['Course Number']

        var geToId = {
            'Breadth Area': 'areaReq',
            'Physical Education': 'peReq',
            'Language': 'langReq',
            'Analyzing Difference': 'analyzingReq',
            'Speaking Intensive': 'speakingReq',
            'Writing Intensive': 'writingReq'
        }

        Object.keys(data).forEach((ge) => {
            if (ge === 'Course Title' || ge === 'Course Number' || !data[ge]) {
                return // this is foreach continue
            }
            const tagId = geToId[ge]
            toggledElts.push(toggleElt(tagId, tagId === 'areaReq' ? data[ge] : null))
        })
        if (!toggledElts.length) {
            toggledElts.push(toggleElt('reqsNone'))
        }
    } 
}

function toggleElt(tagId, area=null) {
    var elt = document.getElementById(tagId)
    if (area) {
        elt.innerText = area
    }
    elt.classList.toggle('hidden')
    return elt
}

$('#addCourse').click(function() {
   var selectedSem = $('#semSelect option:selected').text()
   var selectedCourse = window.selectedCourse

   $.ajax({
       type: "POST",
       url: "addCourse",
       data: JSON.stringify({
           'sem': selectedSem,
           'course': selectedCourse
       }),
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       success: function(response) {
           location.reload();
       }
   })
});