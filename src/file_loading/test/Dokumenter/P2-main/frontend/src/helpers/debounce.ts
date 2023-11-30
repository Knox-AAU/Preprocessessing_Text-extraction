/* eslint-disable @typescript-eslint/no-explicit-any */

// Creates a debounced version of the function that is passed in. See more:
// https://css-tricks.com/debouncing-throttling-explained-examples/
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  time: number
): (...args: Parameters<T>) => void {
  // Save the timeout id inside the scope of this function. If the function
  // returned gets called, this variable gets set.
  let timeout: ReturnType<typeof setTimeout>;

  // Returns the debounced function
  return function (this: unknown, ...args) {
    // Clear the timeout from the previous call (if any)
    clearTimeout(timeout);
    // Create a new timeout and set the id
    timeout = setTimeout(() => {
      // Call the function where `this` is bound to the `this` outside of the
      // function
      fn.apply(this, args);
    }, time);
  };
}
