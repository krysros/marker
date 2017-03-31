<%inherit file="layout.mako"/>  

<div class="panel panel-default">
  <div class="panel-heading">${heading}</div>
  <div class="panel-body">
    ${rendered_form | n}
  </div>
</div>