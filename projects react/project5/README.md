this project covers state lifting and conditional statements for rendering content; 


In React, state lifting means moving shared state from a child component up to the closest common ancestor (parent), so that multiple children can access and update it.

Why do it?
Because React has one-way data flow (data goes down via props, events go up via callbacks). Sibling components can't directly share state with each other.

