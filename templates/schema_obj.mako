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
        <th>${ primary_key_field }</th>
    % for key in schema_entries[0]:
        <th>${key}</th>
    % endfor
    </thead>
    <tbody>
    % for i in schema_entries:
        <tr>
            <td>${i[primary_key_field]}</td>
            % for key, value in i.iteritems():
                % if value != primary_key_field:
                    <td>${value}</td>
                % endif
            % endfor
        </tr>
    % endfor
    </tbody>
</table>