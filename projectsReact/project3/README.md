as there is one hook useState which basically used to set value to count varible . 
ex. const [count,setcount]=useState(10);
as we set value 10 to the count variable respectively. 
see the files . 

theory: 
========================================================================
REACT HOOKS: THE SIMPLE DEFINITION
========================================================================

In the simplest terms, Hooks are special functions that allow you to 
"hook into" React's internal features from inside a simple functional 
component.

Before Hooks, you could only use basic functions to show static data. 
If you wanted the component to remember things or do something 
automatically, you had to use complex "Class Components." Hooks give 
those same "superpowers" to simple functions.

------------------------------------------------------------------------
THE THREE MAIN "SUPERPOWERS" OF HOOKS
------------------------------------------------------------------------
Think of Hooks as tools in a utility belt that you can plug into 
your component:

1. THE POWER OF MEMORY (useState)
   This is the most common hook. It allows a component to remember 
   information (like a user's name, a counter, or whether a menu is 
   open). When this "memory" changes, React automatically updates 
   what you see on the screen.

2. THE POWER OF ACTION (useEffect)
   This hook lets you perform "side effects"—things that happen 
   outside of just displaying text. Examples include:
   - Fetching data from an API.
   - Starting a timer.
   - Changing the title of the browser tab.

3. THE POWER OF SHARING (useContext)
   This allows you to share data (like a "Dark Mode" setting) across 
   many different components without having to pass it down manually 
   like a relay race.
========================================================================

