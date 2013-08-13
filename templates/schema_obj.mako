<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
<script src="http://code.jquery.com/jquery.js"></script>
<script src="/static/js/bootstrap.min.js"></script>

<h2>${title}</h2>
<table class="table table-striped table-bordered" id="info">${schema_info}</table>
<h3>Entries</h3>
<table class="table table-striped table-bordered">
    <% import json %>
    <thead>
    % for key in schema_entries[0]:
        <th>${key}</th>
    % endfor
    </thead>
    <tbody>
    % for i in schema_entries:
        <tr>
        % for key, value in i.iteritems():
            <td>${value}</td>
        % endfor
        </tr>
    % endfor
    </tbody>
</table>