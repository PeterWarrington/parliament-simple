{% for post in site.posts %}
<div>
<h3><a href="{{ post.url }}" style="color: inherit">The film isn't about Facebook: Why The Social Network has the perfect scene</a></h3>
<i>{{ page.date | split: " " | first }}</i>
<p>
{{post.description}}
</p>
</div>

<hr/>
{% endfor %}