function patchtext(selector, oldval, newval) {
  $(selector).filter(function() {return ($(this).html()===oldval)}).text(newval);
  };
