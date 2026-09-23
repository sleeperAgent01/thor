library(ggplot2)
library(ape)
library(ggtree)

setwd("/run/media/pinkpunk/myriad/thor2026/ddradseq/ipyrad/thor_ddrad-2026_outfiles/caster/supplementary/original")

tree <- read.tree("./Thor-caster.nwk")

# Mapeo de nombres cortos -> nombres completos
nombres_largos <- c(
  "Socolofi"        = "Thorichthys socolofi",
  "Helleri"         = "Thorichthys helleri",
  "Maculipinnis"    = "Thorichthys maculipinnis",
  "Aureus"          = "Thorichthys aureus",
  "Callolepis"      = "Thorichthys callolepis",
  "Pasionis"        = "Thorichthys pasionis",
  "Meeki"           = "Thorichthys meeki",
  "Salvini"         = "Trichromis salvini",
  "M_ornatus"       = "Mesoheros ornatus",
  "M_festae"        = "Mesoheros festae",
  "M_atromaculatus" = "Mesoheros atromaculatus"
)

tree$tip.label <- nombres_largos[tree$tip.label]

p_caster <- ggtree(tree, size = 2, color = "black") +
  geom_tree(size = 1, color = "gray") +
  geom_nodelab(geom = "text", nudge_y = 0.27, nudge_x = -0.4, size = 5) +
  geom_tiplab(align = TRUE, hjust = -0.05,
              fontface = "italic", size = 5) +
  xlim(NA, 12) +
  theme_tree() +
  theme(panel.grid = element_blank(),
        axis.title = element_blank(),
        axis.text  = element_blank(),
        axis.ticks = element_blank())

p_caster

#cargando el de svd para homogenización
#homogenizando
#21 de septiemnre, 2026

thorsvd <- read.nexus("./Thor_SVD_bootstrap02_std.tree")

thorTree <- root(phy = thorsvd,
                 outgroup = "Mesoheros atromaculatus",
                 resolve.root = TRUE)

# Forzar el mismo orden de tips que el árbol de CASTER
thorTree <- ape::rotateConstr(thorTree, tree$tip.label)

# Verificar
identical(tree$tip.label, thorTree$tip.label)

p_svd <- ggtree(thorTree, size = 2, color = "black",
                branch.length = "none") +
  geom_tree(size = 1, color = "gray") +
  geom_text2(mapping = aes(label = branch.length,
                           subset = !is.na(as.numeric(branch.length)) &
                             as.numeric(branch.length) > 80),
             nudge_x = -0.5, nudge_y = 0.3, size = 5) +
  geom_tiplab(align = TRUE, hjust = -0.05,
              fontface = "italic", size = 5) +
  xlim(NA, 12) +
  theme_tree() +
  theme(panel.grid  = element_blank(),
        axis.title  = element_blank(),
        axis.text   = element_blank(),
        axis.ticks  = element_blank())

p_svd

#combinando ambos plots
cowplot::plot_grid(p_caster,p_svd)

ggsave("Thor-caster_tree.pdf", p_caster, width = 8, height = 6, dpi = 300)
ggsave("Thor-caster_tree.png", p_caster, width = 8, height = 6, dpi = 300)