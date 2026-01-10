{% for post in site.posts %}
<div>
<h3><a href="{{ post.url }}" style="color: inherit; margin-bottom: 0;">{{ post.title }}</a></h3>

<p style="margin-top: 9px;">
<span style="font-weight: bold; font-style: italic; color: #FFC; padding-right: 8px;">{{ post.date | split: " " | first }}</span>

{{post.description}}
</p>

</div>

<hr/>
{% endfor %}