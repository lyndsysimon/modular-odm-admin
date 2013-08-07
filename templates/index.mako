<link rel="stylesheet" src="../static/css/bootstrap.min.css" />

<h3>Hello</h3>
<p>
   % for key, value in schemas.iteritems():
    <a href="/${key}">${key}</a> ... ${type(value._storage[0]).__name__}</p>
   % endfor
##    ${schemas}</p>