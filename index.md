> Presenting the most notable speeches of the House of Commons and the House of Lords every week, without spin.
> **Know the debates of our time.**

{% for post in site.posts %}
<div class="post">
<h3 style="margin-bottom: 0;"><a href="{{ post.url }}" style="color: inherit;">{{ post.title }}</a></h3>

<p style="margin-top: 9px;">
<span style="font-weight: bold; font-style: italic; color: #FFC; padding-right: 8px;">{{ post.date | split: " " | first }}</span>

{{post.description}}
</p>

</div>

<hr/>
{% endfor %}