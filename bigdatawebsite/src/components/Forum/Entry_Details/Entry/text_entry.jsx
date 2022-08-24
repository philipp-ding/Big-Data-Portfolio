
import React from 'react';
import "./text_entry.css"
const TextEntry = ({ name, lastname, email, body }) => {
  return (
<div class="container">
  <div class="User">
      <p>{name} {lastname}: {email}</p>
  </div>
  <div class="Message"><p>{body}</p></div>
</div>
  
  );
};

export default TextEntry;