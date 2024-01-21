export function remove_element(class_name) {
  let elements = document.querySelectorAll(`.${class_name}`);
  // console.log(elements, "ELEMENTSSSSSSSSSSSSS");
  elements.forEach(function (ele) {
    ele.parentNode.removeChild(ele);
  });
}
