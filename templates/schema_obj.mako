<h3>${title}</h3>
<p>${info}</p>
<h2>Entries</h2>
<p>
    % for i in entries:
        ${i} <a href="/${title}/${i[primary_name]}/edit">edit</a><br>
    % endfor
</p>
##<p>
##   % for key, value in info.iteritems():
##    ${key} ... ${value}</p>
##   % endfor