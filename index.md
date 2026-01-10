{% for post in site.posts %}
<div>
<h3><a href="{{ post.url }}" style="color: inherit">{{ post.title }}</a></h3>
<i>{{ post.date | split: " " | first }}</i>
<p>
{{post.description}}
</p>
</div>

<hr/>
{% endfor %}