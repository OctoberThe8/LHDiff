// Source - https://stackoverflow.com/a
// Posted by xdazz, modified by community. See post 'Timeline' for change history
// Retrieved 2025-11-28, License - CC BY-SA 3.0

var arr = [
  {url: "link 1"},
  {url: "link 2"},
  {url: "link 3"}
];

arr = arr.filter(function(el){
  return el.url !== "link 2";
});

// Minimal completion so the file represents a full runnable example
console.log(arr);
