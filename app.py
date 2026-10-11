
import streamlit as st
import requests

st.set_page_config(page_title="Anime Finder", page_icon="🍥")

st.title("🍥 Anime Finder")
st.write("Discover anime, ratings, episodes, and stories.")

anime_name = st.text_input("Enter an anime name", placeholder="Try Naruto")

if st.button("Search Anime"):
    if not anime_name.strip():
        st.warning("Please enter an anime name.")
    else:
        with st.spinner("Searching anime..."):
            try:
                response = requests.get(
                    "https://api.jikan.moe/v4/anime",
                    params={"q": anime_name.strip(), "limit": 5},
                    timeout=15,
                )
                response.raise_for_status()
                results = response.json().get("data", [])

                if not results:
                    st.info("No anime found. Try another name.")
                else:
                    for anime in results:
                        title = anime.get("title_english") or anime.get("title")
                        st.subheader(f"🍥 {title}")

                        image_url = anime.get("images", {}).get(
                            "jpg", {}
                        ).get("large_image_url")

                        if image_url:
                            st.image(image_url, width=220)

                        st.write(
                            f"⭐ Rating: {anime.get('score') or 'N/A'} / 10"
                        )
                        st.write(
                            f"🎬 Episodes: {anime.get('episodes') or 'Unknown'}"
                        )
                        st.write(
                            f"📅 Year: {anime.get('year') or 'Unknown'}"
                        )
                        st.write(
                            anime.get("synopsis") or "No description available."
                        )
                        st.link_button("View on MyAnimeList", anime["url"])
                        st.divider()

            except requests.RequestException:
                st.error("Anime search is temporarily unavailable. Try again later.")

