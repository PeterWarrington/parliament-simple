> Presenting the most notable speeches of the House of Commons and the House of Lords every week, without spin, and without the boring bits.
> **Know the debates of our time.**

<hr/>

{% for post in site.posts %}
<div class="post">
<h3 style="margin-bottom: 0;"><a href="{{ post.url }}" style="color: inherit;">{{ post.title }}</a></h3>

<p style="margin-top: 9px;">
<span style="font-weight: bold; font-style: italic; opacity: 0.7; padding-right: 4px;">
        {% if post.author %}
        ✏️ {{post.author}},
        {% endif %}

        {{ post.date | split: " " | first }}
</span>

{{post.description}}
</p>

</div>

<hr/>
{% endfor %}

<small>
📡 <a href="/feed.xml">RSS Feed</a>
</small>