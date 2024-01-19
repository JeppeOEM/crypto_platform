function unpack(cond) {
  return (
    cond
      .flat()
      // each obj returns as array, with values joined together in a string
      // there is only 1 val pr array.
      .map((obj) => Object.values(obj).join("")) //* implicit return *
      .join(" ")
  );
}
