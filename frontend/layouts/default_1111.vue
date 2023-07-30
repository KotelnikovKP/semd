<template>
    <div>
        <Navbar_1111 />
        <Nuxt />
        <Footer />
    </div>
</template>
  
  
<script>
import Navbar_1111 from "~/components/Navbar_1111";
import Footer from "@/components/Footer";

export default {
    components: {
        Navbar_1111,
        Footer,
    },
    head() {
        return {
            link: [
                { rel: "canonical", href: `http://localhost:3000${this.$route.path}` }
            ]
        }
    }
}
</script>
  
<style></style>