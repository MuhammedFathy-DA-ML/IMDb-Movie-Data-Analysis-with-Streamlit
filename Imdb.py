import streamlit as st
from PIL import Image


#st.title('IMDb Movies Analysis')

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg" alt="IMDb Logo" width="100">
        <h1 style="color: #F5C518; margin-top: 10px;">IMDb Movies Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)


image = Image.open('D:\\PYTHON PROJECTS\\top-20-movies-in-history-according-to-imdb-pick-5-the-rest-v0-5cqqa01c026e1.webp') 
st.image(image, caption='Top-20-movies-in-history', use_container_width=True)



# إضافة بعض النصوص
#st.write("This is a simple Streamlit app for movie analysis using IMDb data.")

st.markdown("---")

import streamlit as st
import pandas as pd
import plotly.express as px


# تحميل البيانات
df = pd.read_csv("tmdb-movies.csv")
df = df.drop_duplicates().dropna()
df = df[(df["budget_adj"] > 0) & (df["revenue_adj"] > 0)]

# إنشاء الرسمة
fig = px.scatter(
    df,
    x="budget_adj",
    y="revenue_adj",
    hover_data=["original_title", "release_year"],
    title="Adjusted Budget vs Adjusted Revenue",
    labels={"budget_adj": "Adjusted Budget", "revenue_adj": "Adjusted Revenue"},
    opacity=0.6,
    width=700,
    height=450
)
fig.update_traces(marker=dict(size=5))

# عرض الرسمة في Streamlit
st.plotly_chart(fig)



st.markdown("---")


import plotly.express as px

# تجميع عدد الأفلام لكل سنة
films_per_year = df.groupby("release_year")["id"].count().reset_index()
films_per_year.columns = ["release_year", "film_count"]

# رسم عدد الأفلام سنويًا
fig2 = px.line(
    films_per_year,
    x="release_year",
    y="film_count",
    title="Number of Movies Released per Year",
    labels={"release_year": "Release Year", "film_count": "Number of Movies"},
    markers=True,
    width=700,
    height=450
)
fig2.update_traces(line=dict(color="royalblue"), marker=dict(size=6))
st.plotly_chart(fig2)

st.markdown("---")

genres_series = df["genres"].dropna().str.split("|").explode()

# حساب تكرار كل نوع
genre_counts = genres_series.value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

# رسم Bar Chart
fig3 = px.bar(
    genre_counts.sort_values("count", ascending=False).head(10),  # نعرض أشهر 10
    x="genre",
    y="count",
    title="Top 10 Most Frequent Movie Genres",
    labels={"genre": "Genre", "count": "Number of Movies"},
    color="count",
    color_continuous_scale="Blues",
    width=700,
    height=450
)
st.plotly_chart(fig3)

st.markdown("---")

df_genres = df[["genres", "revenue_adj"]].dropna()
df_genres = df_genres[df_genres["revenue_adj"] > 0]
df_genres = df_genres.assign(genres=df_genres["genres"].str.split("|")).explode("genres")

# تجميع الإيرادات حسب النوع
genre_revenue = df_genres.groupby("genres")["revenue_adj"].mean().reset_index()
genre_revenue.columns = ["genre", "avg_revenue"]

# رسم Bar Chart
fig4 = px.bar(
    genre_revenue.sort_values("avg_revenue", ascending=False).head(10),
    x="genre",
    y="avg_revenue",
    title="Top 10 Genres by Average Adjusted Revenue",
    labels={"genre": "Genre", "avg_revenue": "Average Adjusted Revenue"},
    color="avg_revenue",
    color_continuous_scale="Viridis",
    width=700,
    height=450
)
st.plotly_chart(fig4)

st.markdown("---")

df_roi = df.copy()
df_roi = df_roi[(df_roi["budget_adj"] > 0) & (df_roi["revenue_adj"] > 0)]
df_roi["ROI"] = (df_roi["revenue_adj"] - df_roi["budget_adj"]) / df_roi["budget_adj"]

# تفجير الأنواع
df_roi = df_roi[["genres", "ROI"]].dropna()
df_roi = df_roi.assign(genres=df_roi["genres"].str.split("|")).explode("genres")

# حساب متوسط ROI لكل نوع
genre_roi = df_roi.groupby("genres")["ROI"].mean().reset_index()
genre_roi.columns = ["genre", "avg_ROI"]

# رسم Bar Chart
fig5 = px.bar(
    genre_roi.sort_values("avg_ROI", ascending=False).head(10),
    x="genre",
    y="avg_ROI",
    title="Top 10 Genres by Average ROI",
    labels={"genre": "Genre", "avg_ROI": "Average ROI"},
    color="avg_ROI",
    color_continuous_scale="Plasma",
    width=700,
    height=450
)
st.plotly_chart(fig5)


st.markdown("---")

df_rating = df[["genres", "vote_average"]].dropna()

# تفجير الأنواع
df_rating = df_rating.assign(genres=df_rating["genres"].str.split("|")).explode("genres")

# حساب متوسط التقييم حسب النوع
genre_rating = df_rating.groupby("genres")["vote_average"].mean().reset_index()
genre_rating.columns = ["genre", "avg_rating"]

# رسم Bar Chart
fig6 = px.bar(
    genre_rating.sort_values("avg_rating", ascending=False).head(10),
    x="genre",
    y="avg_rating",
    title="Top 10 Genres by Average Rating",
    labels={"genre": "Genre", "avg_rating": "Average Rating"},
    color="avg_rating",
    color_continuous_scale="Tealgrn",
    width=700,
    height=450
)
st.plotly_chart(fig6)

st.markdown("---")

df_runtime = df[["runtime", "revenue_adj"]].dropna()
df_runtime = df_runtime[(df_runtime["runtime"] > 0) & (df_runtime["revenue_adj"] > 0)]

# رسم scatter تفاعلي
fig7 = px.scatter(
    df_runtime,
    x="runtime",
    y="revenue_adj",
    title="Movie Runtime vs Adjusted Revenue",
    labels={"runtime": "Movie Runtime (minutes)", "revenue_adj": "Adjusted Revenue"},
    opacity=0.5,
    width=700,
    height=450
)
fig7.update_traces(marker=dict(size=5, color="indigo"))
st.plotly_chart(fig7)

st.markdown("---")

df = pd.read_csv("tmdb-movies.csv")

# استخدام العمود الصحيح لعنوان الفيلم والإيرادات
top_revenue = df[["original_title", "revenue"]].dropna()

# تصفية أعلى 10 أفلام من حيث الإيرادات
top_revenue = top_revenue.sort_values("revenue", ascending=False).head(10)

# رسم Bar Chart تفاعلي
fig8 = px.bar(
    top_revenue,
    x="original_title",
    y="revenue",
    title="Top 10 Movies by Revenue",
    labels={"original_title": "Movie Title", "revenue": "Revenue (USD)"},
    color="revenue",
    color_continuous_scale="Viridis",
    width=800,
    height=500
)

fig8.update_layout(xaxis_tickangle=-45)  # تدوير أسماء الأفلام
st.plotly_chart(fig8)


st.markdown("---")
 #استخراج أفضل المخرجين من حيث عدد الأفلام
top_directors = df['director'].value_counts().nlargest(10).index
df_top_directors = df[df['director'].isin(top_directors)]

# رسم متوسط الإيرادات لهؤلاء المخرجين
import plotly.express as px
fig9 = px.bar(
    df_top_directors.groupby('director')['revenue_adj'].mean().reset_index(),
    x='director',
    y='revenue_adj',
    title='Top Directors by Average Adjusted Revenue',
    labels={'revenue_adj': 'Avg Adjusted Revenue', 'director': 'Director'},
    color='revenue_adj',
    color_continuous_scale='blues'
)
fig9.update_layout(xaxis_tickangle=-45, width=700, height=450)
st.plotly_chart(fig9)

st.markdown("---")
# رسم العلاقة بين الميزانية والتقييم
fig10 = px.scatter(
    df,
    x='budget_adj',
    y='vote_average',
    hover_data=['original_title', 'release_year'],
    title='Adjusted Budget vs Average Rating',
    labels={'budget_adj': 'Adjusted Budget', 'vote_average': 'Average Rating'},
    opacity=0.5,
    width=700,
    height=450
)
fig10.update_traces(marker=dict(size=6, color='orange'))
st.plotly_chart(fig10)

st.markdown("---")

import pandas as pd
import plotly.express as px
import streamlit as st

# عنوان الصفحة
st.title("🎬 Spielberg's Movie Analysis by Genre")

# تحميل البيانات
df = pd.read_csv("tmdb-movies.csv")
df = df.drop_duplicates().dropna()
df = df[(df["budget_adj"] > 0) & (df["revenue_adj"] > 0)]

# إنشاء عمود الأرباح المعدلة
df["profit_adj"] = df["revenue_adj"] - df["budget_adj"]

# تصفية أفلام ستيفن سبيلبرغ
spielberg_df = df[df["director"] == "Steven Spielberg"]

# =======================
# 11. أكثر الأنواع إخراجًا
# =======================
st.subheader("11️⃣ Top Genres by Steven Spielberg")
genre_counts = spielberg_df["genres"].value_counts().nlargest(10).reset_index()
genre_counts.columns = ["Genre", "Count"]

fig11 = px.bar(
    genre_counts,
    x="Genre",
    y="Count",
    title="Top Genres by Steven Spielberg",
    width=700,
    height=400
)
st.plotly_chart(fig11)

st.markdown("---")

# =======================
# 12. متوسط التقييم لكل نوع
# =======================
st.subheader("12️⃣ Average Rating by Genre")
rating_by_genre = spielberg_df.groupby("genres")["vote_average"].mean().reset_index()
rating_by_genre.columns = ["Genre", "Average Rating"]

fig12 = px.bar(
    rating_by_genre.sort_values("Average Rating", ascending=False),
    x="Genre",
    y="Average Rating",
    title="Average Rating of Spielberg's Movies by Genre",
    width=700,
    height=400
)
st.plotly_chart(fig12)

st.markdown("---")

# =======================
# 13. متوسط الأرباح حسب النوع
# =======================
st.subheader("13️⃣ Average Profit by Genre")
profit_by_genre = spielberg_df.groupby("genres")["profit_adj"].mean().reset_index()
profit_by_genre.columns = ["Genre", "Average Profit"]

fig13 = px.bar(
    profit_by_genre.sort_values("Average Profit", ascending=False),
    x="Genre",
    y="Average Profit",
    title="Average Profit of Spielberg's Movies by Genre",
    width=700,
    height=400
)
st.plotly_chart(fig13)

st.markdown("---")


df = df[(df["budget_adj"] > 0) & (df["revenue_adj"] > 0)]

# إنشاء عمود الأرباح المعدلة
df["profit_adj"] = df["revenue_adj"] - df["budget_adj"]

# تصفية أفلام ستيفن سبيلبرغ
spielberg_df = df[df["director"] == "Steven Spielberg"]

# متوسط مدة الأفلام حسب النوع
runtime_by_genre = spielberg_df.groupby("genres")["runtime"].mean().reset_index()
runtime_by_genre.columns = ["Genre", "Average Runtime"]

fig14 = px.bar(
    runtime_by_genre.sort_values("Average Runtime", ascending=False),
    x="Genre",
    y="Average Runtime",
    title="Average Runtime of Spielberg's Movies by Genre",
    width=700,
    height=400
)

st.plotly_chart(fig14)

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # عنوان الصفحة
# st.title("Top 10 Movies by Revenue")

# # تحميل البيانات
# df = pd.read_csv("tmdb-movies.csv")  # تأكد إن الملف ده في نفس المجلد

# # التحقق من الأعمدة
# if "original_title" in df.columns and "revenue" in df.columns:
#     top_revenue = df[["original_title", "revenue"]].dropna()
#     top_revenue = top_revenue.sort_values("revenue", ascending=False).head(10)

#     # رسم الرسمة
#     fig = px.bar(
#         top_revenue,
#         x="original_title",
#         y="revenue",
#         title="Top 10 Movies by Revenue",
#         labels={"original_title": "Movie Title", "revenue": "Revenue (USD)"},
#         color="revenue",
#         color_continuous_scale="Viridis",
#         width=800,
#         height=500
#     )
#     fig.update_layout(xaxis_tickangle=-45)

#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.warning("Columns not found in the dataset.")
