> Presenting the most notable debates of the House of Commons and the House of Lords, without spin. <br/> <b>Know the debates of our time.</b>

{% include subscribe.html %}

<hr/>



{% for post in site.posts %}
<div class="post">
<h3 style="margin-bottom: 0;"><a href="{{ post.url }}" style="color: inherit;">{{ post.title }}</a></h3>

<p style="margin-top: 9px;">
<span style="font-weight: bold; font-style: italic; opacity: 0.7; padding-right: 4px;">
        ✏️ {{ post.date | split: " " | first }}
</span>

{{post.description}}
</p>

</div>

<hr/>
{% endfor %}

<small>
📡 <a href="/feed.xml">RSS Feed</a>
</small>