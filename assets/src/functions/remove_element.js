export function remove_element(class_name) {
  let elements = document.querySelectorAll(`.${class_name}`);

  elements.forEach(function (ele) {
    ele.parentNode.removeChild(ele);
  });
}
