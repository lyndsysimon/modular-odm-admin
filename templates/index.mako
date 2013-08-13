<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
<script src="http://code.jquery.com/jquery.js"></script>
<script src="/static/js/bootstrap.min.js"></script>

<h2>Center for Fantasy Football</h2>
<p class="prettyprint">
   % for key, value in schemas.iteritems():
    <a href="/${key}">${key}</a> ... ${type(value._storage[0]).__name__}</p>
   % endfor
##    ${schemas}</p>