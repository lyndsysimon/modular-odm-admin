<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
<script src="http://code.jquery.com/jquery.js"></script>
<script src="/static/js/bootstrap.min.js"></script>
<script src="/static/js/json-to-html-table.js"></script>

<h2>${title}</h2>
<table class="table table-striped table-bordered" id="info"></table>
<h3>Entries</h3>
<p >
    % for i in entries:
        <span class="span4"> ${i} </span>
            <a href="/${title}/${i[primary_name]}/edit">edit</a><br>
    % endfor
</p>
<table class="table table-striped table-bordered" id="entries"></table>


<script type="text/javascript">
##    var table = ConvertJsonToTable(${entries});
##    var schema = ConvertJsonToTable([${info}]);
##    $('#entries').html(table);
##    $('#info').html(schema);

</script>
##<p>
##   % for key, value in info.iteritems():
##    ${key} ... ${value}</p>
##   % endfor