document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
      var $notification = $delete.parentNode;
  
      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    });
  });

  var e = document.getElementById("nurseID");
  var strNurse = e.value;

  var p = document.getElementById("period");
  var strPeriod = p.value;
  
  var d = document.getElementById("diseaseid");
  var strDisease = d.value;

  var f = document.getElementById("filter_disease");
  var strFilter = f.value;

  var pe = document.getElementById("filter_period");
  var strPeriod = pe.value;